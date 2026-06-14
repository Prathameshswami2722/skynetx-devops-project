import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, g, jsonify, redirect, render_template, request, url_for
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "skynetx.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "skynetx-dev-secret"
app.config["DATABASE"] = DATABASE

REQUEST_COUNTER = Counter(
    "skynetx_http_requests_total",
    "Total HTTP requests received by the SkyNetX application",
    ["method", "endpoint"],
)
TELEMETRY_COUNTER = Counter(
    "skynetx_telemetry_events_ingested_total",
    "Total telemetry events ingested by the SkyNetX platform",
)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(app.config["DATABASE"])
    cursor = db.cursor()
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS drones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drone_id TEXT UNIQUE NOT NULL,
            operator_name TEXT NOT NULL,
            drone_type TEXT NOT NULL,
            operational_region TEXT NOT NULL,
            purpose TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drone_id TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            altitude REAL NOT NULL,
            speed REAL NOT NULL,
            battery_percentage INTEGER NOT NULL,
            signal_status TEXT NOT NULL,
            weather_condition TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS flight_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drone_id TEXT NOT NULL,
            source_location TEXT NOT NULL,
            destination_location TEXT NOT NULL,
            flight_purpose TEXT NOT NULL,
            requested_altitude REAL NOT NULL,
            approval_status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        );
        """
    )
    db.commit()
    db.close()


init_db()


def query_one(query, params=()):
    return get_db().execute(query, params).fetchone()


def query_all(query, params=()):
    return get_db().execute(query, params).fetchall()


def get_latest_telemetry_rows():
    return query_all(
        """
        SELECT t.*, d.operator_name, d.operational_region, d.status AS drone_status
        FROM telemetry t
        JOIN (
            SELECT drone_id, MAX(created_at) AS max_created_at
            FROM telemetry
            GROUP BY drone_id
        ) latest ON latest.drone_id = t.drone_id AND latest.max_created_at = t.created_at
        LEFT JOIN drones d ON d.drone_id = t.drone_id
        ORDER BY t.created_at DESC
        """
    )


def build_airspace_rows():
    latest_requests = {
        row["drone_id"]: row
        for row in query_all(
            """
            SELECT fr.*
            FROM flight_requests fr
            JOIN (
                SELECT drone_id, MAX(created_at) AS max_created_at
                FROM flight_requests
                GROUP BY drone_id
            ) latest ON latest.drone_id = fr.drone_id AND latest.max_created_at = fr.created_at
            """
        )
    }

    rows = []
    for telemetry in get_latest_telemetry_rows():
        request_row = latest_requests.get(telemetry["drone_id"])
        route_status = "Monitoring"
        if request_row:
            route_status = request_row["approval_status"]

        collision_risk = "Low"
        if float(telemetry["altitude"]) > 400 or float(telemetry["speed"]) > 120:
            collision_risk = "Medium"
        if telemetry["signal_status"] == "Lost" or "storm" in telemetry["weather_condition"].lower():
            collision_risk = "High"

        region_status = "Stable"
        if telemetry["signal_status"] != "Strong":
            region_status = "Communication Watch"
        if "storm" in telemetry["weather_condition"].lower():
            region_status = "Weather Risk"

        rows.append(
            {
                "drone_id": telemetry["drone_id"],
                "operator_name": telemetry["operator_name"] or "Unknown",
                "operational_region": telemetry["operational_region"] or "Unassigned",
                "route_status": route_status,
                "collision_risk": collision_risk,
                "region_status": region_status,
                "altitude": telemetry["altitude"],
                "speed": telemetry["speed"],
                "weather_condition": telemetry["weather_condition"],
            }
        )
    return rows


def build_emergency_alerts():
    alerts = []
    for telemetry in get_latest_telemetry_rows():
        drone_id = telemetry["drone_id"]
        region = telemetry["operational_region"] or "Unknown Region"
        if telemetry["battery_percentage"] <= 20:
            alerts.append(
                {
                    "drone_id": drone_id,
                    "alert_type": "Low Battery",
                    "severity": "High",
                    "details": f"Battery at {telemetry['battery_percentage']}% in {region}.",
                }
            )
        if telemetry["signal_status"] == "Lost" or telemetry["drone_status"] == "Communication Lost":
            alerts.append(
                {
                    "drone_id": drone_id,
                    "alert_type": "Communication Lost",
                    "severity": "Critical",
                    "details": f"Command link instability detected in {region}.",
                }
            )
        if "storm" in telemetry["weather_condition"].lower() or "wind" in telemetry["weather_condition"].lower():
            alerts.append(
                {
                    "drone_id": drone_id,
                    "alert_type": "Weather Risk",
                    "severity": "Medium",
                    "details": f"Weather condition reported as {telemetry['weather_condition']}.",
                }
            )
        if float(telemetry["altitude"]) > 450 or float(telemetry["speed"]) > 140:
            alerts.append(
                {
                    "drone_id": drone_id,
                    "alert_type": "Collision Risk",
                    "severity": "Critical",
                    "details": "Altitude or speed exceeds safe operating threshold.",
                }
            )
        if telemetry["battery_percentage"] <= 10:
            alerts.append(
                {
                    "drone_id": drone_id,
                    "alert_type": "Emergency Landing Required",
                    "severity": "Critical",
                    "details": "Immediate emergency landing coordination required.",
                }
            )
    return alerts


@app.before_request
def track_requests():
    REQUEST_COUNTER.labels(request.method, request.endpoint or "unknown").inc()


@app.route("/")
@app.route("/dashboard")
def dashboard():
    db = get_db()
    total_drones = db.execute("SELECT COUNT(*) FROM drones").fetchone()[0]
    active_drones = db.execute(
        "SELECT COUNT(*) FROM drones WHERE status = 'Active'"
    ).fetchone()[0]
    pending_approvals = db.execute(
        "SELECT COUNT(*) FROM flight_requests WHERE approval_status = 'Pending'"
    ).fetchone()[0]
    telemetry_events = db.execute("SELECT COUNT(*) FROM telemetry").fetchone()[0]
    emergency_alerts = len(build_emergency_alerts())
    recent_flights = query_all(
        """
        SELECT drone_id, source_location, destination_location, approval_status, created_at
        FROM flight_requests
        ORDER BY created_at DESC
        LIMIT 5
        """
    )

    return render_template(
        "dashboard.html",
        total_drones=total_drones,
        active_drones=active_drones,
        pending_approvals=pending_approvals,
        emergency_alerts=emergency_alerts,
        telemetry_events=telemetry_events,
        recent_flights=recent_flights,
    )


@app.route("/drones/add", methods=["GET", "POST"])
def add_drone():
    if request.method == "POST":
        form = request.form
        try:
            get_db().execute(
                """
                INSERT INTO drones (
                    drone_id, operator_name, drone_type, operational_region, purpose, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    form["drone_id"].strip(),
                    form["operator_name"].strip(),
                    form["drone_type"].strip(),
                    form["operational_region"].strip(),
                    form["purpose"].strip(),
                    form["status"].strip(),
                    datetime.utcnow().isoformat(),
                ),
            )
            get_db().commit()
            flash("Drone registered successfully in the SkyNetX fleet.", "success")
            return redirect(url_for("drone_list"))
        except sqlite3.IntegrityError:
            flash("Drone ID already exists. Use a unique SkyNetX drone identifier.", "danger")

    return render_template("add_drone.html")


@app.route("/drones")
def drone_list():
    drones = query_all("SELECT * FROM drones ORDER BY created_at DESC")
    return render_template("drone_list.html", drones=drones)


@app.route("/telemetry", methods=["GET", "POST"])
def telemetry_update():
    drones = query_all("SELECT drone_id FROM drones ORDER BY drone_id")
    if request.method == "POST":
        form = request.form
        drone = query_one("SELECT drone_id FROM drones WHERE drone_id = ?", (form["drone_id"],))
        if not drone:
            flash("Telemetry can only be logged for a registered SkyNetX drone.", "danger")
            return render_template("telemetry_update.html", drones=drones)

        get_db().execute(
            """
            INSERT INTO telemetry (
                drone_id, latitude, longitude, altitude, speed, battery_percentage,
                signal_status, weather_condition, timestamp, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                form["drone_id"].strip(),
                float(form["latitude"]),
                float(form["longitude"]),
                float(form["altitude"]),
                float(form["speed"]),
                int(form["battery_percentage"]),
                form["signal_status"].strip(),
                form["weather_condition"].strip(),
                form["timestamp"].strip(),
                datetime.utcnow().isoformat(),
            ),
        )
        get_db().commit()
        TELEMETRY_COUNTER.inc()
        flash("Telemetry event ingested by SkyNetX operations.", "success")
        return redirect(url_for("airspace_monitoring"))

    return render_template("telemetry_update.html", drones=drones)


@app.route("/flight-authorization", methods=["GET", "POST"])
def flight_authorization():
    drones = query_all("SELECT drone_id FROM drones ORDER BY drone_id")
    if request.method == "POST":
        form = request.form
        get_db().execute(
            """
            INSERT INTO flight_requests (
                drone_id, source_location, destination_location, flight_purpose,
                requested_altitude, approval_status, created_at
            ) VALUES (?, ?, ?, ?, ?, 'Pending', ?)
            """,
            (
                form["drone_id"].strip(),
                form["source_location"].strip(),
                form["destination_location"].strip(),
                form["flight_purpose"].strip(),
                float(form["requested_altitude"]),
                datetime.utcnow().isoformat(),
            ),
        )
        get_db().commit()
        flash("Flight request submitted for authorization review.", "success")
        return redirect(url_for("admin_approval"))

    return render_template("flight_authorization.html", drones=drones)


@app.route("/admin-approval", methods=["GET", "POST"])
def admin_approval():
    if request.method == "POST":
        request_id = request.form["request_id"]
        decision = request.form["decision"]
        get_db().execute(
            "UPDATE flight_requests SET approval_status = ? WHERE id = ?",
            (decision, request_id),
        )
        get_db().commit()
        flash(f"Flight request {decision.lower()} successfully.", "info")
        return redirect(url_for("admin_approval"))

    requests_list = query_all(
        "SELECT * FROM flight_requests ORDER BY created_at DESC"
    )
    return render_template("admin_approval.html", requests_list=requests_list)


@app.route("/airspace-monitoring")
def airspace_monitoring():
    monitoring_rows = build_airspace_rows()
    active_drones = [row for row in monitoring_rows if row["route_status"] != "Rejected"]
    return render_template(
        "airspace_monitoring.html",
        monitoring_rows=monitoring_rows,
        active_drones_count=len(active_drones),
    )


@app.route("/emergency-response")
def emergency_response():
    alerts = build_emergency_alerts()
    return render_template("emergency_response.html", alerts=alerts)


@app.route("/health")
def health():
    return jsonify(
        {"status": "healthy", "service": "SkyNetX Drone Traffic Management"}
    )


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
