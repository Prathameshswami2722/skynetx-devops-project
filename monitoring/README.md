# SkyNetX Monitoring

This folder contains simple Prometheus and Grafana support files for the SkyNetX Drone Traffic Management Platform.

## Purpose
SkyNetX depends on operational visibility because the platform manages drone registration, telemetry ingestion, flight approvals, airspace monitoring, and emergency response. Monitoring helps detect failures before they become business or safety incidents.

## Included Files
- `prometheus.yml`
- `alert-rules.yml`
- `grafana-dashboard.json`

## Prometheus Role
Prometheus collects metrics from the SkyNetX Flask application. The application already exposes a `/metrics` endpoint using `prometheus_client`.

Prometheus can be used to observe:

- whether the application is up
- HTTP request volume
- telemetry event ingestion activity
- future infrastructure metrics after Kubernetes monitoring is expanded

## Alerting Role
The alert rules include basic example alerts for:

- app down
- high request count
- pod or service unavailable

These alerts are intentionally simple for college demonstration and can be extended later.

## Grafana Role
Grafana is used to visualize Prometheus data for the SkyNetX platform. The sample dashboard includes panels for:

- app availability
- HTTP request count
- telemetry ingestion activity
- explanation area for Kubernetes pod status
- note about Python and Flask metrics

## How It Fits the SkyNetX Case Study
In the SkyNetX business scenario, real-time monitoring is important because outages, delayed telemetry, or service unavailability can affect logistics, emergency response, agriculture operations, and government drone missions. Prometheus and Grafana help support centralized monitoring and faster response.
