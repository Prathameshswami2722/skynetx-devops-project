# Project SkyNetX

## Problem Statement Summary
Project SkyNetX is based on a DevOps case study about a global drone traffic management platform used by logistics providers, emergency response agencies, agricultural enterprises, and government organizations. The real challenge is to support very large-scale autonomous drone operations while handling telemetry ingestion, airspace coordination, flight approvals, outages, region failures, security risks, and monitoring gaps.

## Objective
The objective of this application is to build a small but functional business application that represents the SkyNetX Drone Traffic Management Platform. This app serves as the core demo system on top of which DevOps practices and tools such as Docker, Jenkins, Terraform, Kubernetes, Prometheus, Grafana, ELK Stack, and Vault can later be applied.

## Features
- Dashboard with total registered drones, active drones, pending flight approvals, emergency alerts, and telemetry events received
- Drone registration module for fleet onboarding
- Drone list page for viewing all registered autonomous aircraft
- Telemetry update module for operational flight data submission
- Flight authorization request module with default pending approval workflow
- Admin approval console to approve or reject drone flight requests
- Airspace monitoring page showing active drones, route status, collision risk level, and region status
- Emergency response page highlighting low battery, communication loss, weather risk, collision risk, and emergency landing conditions
- `/health` JSON endpoint for service health validation
- `/metrics` endpoint for Prometheus monitoring

## Tech Stack
- Python 3
- Flask
- SQLite
- Bootstrap 5
- prometheus_client

## Folder Structure
```text
app.py
requirements.txt
Dockerfile
.dockerignore
docker-compose.yml
templates/
static/
README.md
```

## How to Run Locally
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask application:
   ```bash
   python app.py
   ```
5. Open the application in your browser:
   ```text
   http://127.0.0.1:5000
   ```

## Run with Docker
1. Build the Docker image:
   ```bash
   docker build -t skynetx-app .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 skynetx-app
   ```
3. Open the application in your browser:
   ```text
   http://127.0.0.1:5000
   ```

## Run with Docker Compose
1. Build and start the application:
   ```bash
   docker-compose up --build
   ```
2. Run in detached mode if needed:
   ```bash
   docker-compose up -d --build
   ```
3. Stop the application:
   ```bash
   docker-compose down
   ```

## DevOps Case Study Relevance
This application is intentionally designed around the SkyNetX college case study rather than as a generic drone app. Its modules represent the same operational areas discussed in the problem statement:

- fleet onboarding for large distributed drone operations
- telemetry ingestion for operational visibility
- flight authorization and approvals for controlled airspace usage
- airspace monitoring for route and regional awareness
- emergency response handling for safety incidents
- health and metrics endpoints for observability and future DevOps integration

In later stages, this app can be containerized, deployed through CI/CD pipelines, scaled across infrastructure, monitored through dashboards, secured with secrets management, and used to demonstrate disaster recovery and resilience patterns from the SkyNetX DevOps ecosystem.

This Docker setup is intentionally simple for a college DevOps demonstration. It packages the Flask application into a portable container so the same SkyNetX app can later be used with Jenkins pipelines, Kubernetes deployments, Terraform-managed infrastructure, and observability tools in the broader DevOps case study.
