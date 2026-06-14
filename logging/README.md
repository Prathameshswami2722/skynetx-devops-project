# SkyNetX Logging with ELK Stack

This folder contains a simple ELK Stack demo setup for the SkyNetX DevOps project.

## Included Files
- `docker-compose-elk.yml`
- `logstash.conf`
- `filebeat.yml`

## Purpose
The goal is to show how SkyNetX application and operational logs can be centralized, searched, and analyzed. In a drone traffic management platform, logs are useful for troubleshooting telemetry failures, emergency alerts, flight approvals, and security incidents.

## ELK Components
- Elasticsearch stores and indexes logs.
- Logstash receives and processes logs.
- Kibana provides dashboards and log search.
- Filebeat can ship application log files into Logstash.

## Sample Log Patterns for SkyNetX
Typical log events that can be collected:

- drone registration events
- telemetry update events
- flight approval actions
- emergency alert generation
- error events and failures

Example patterns:

```text
Drone registered successfully in the SkyNetX fleet.
Telemetry event ingested by SkyNetX operations.
Flight request approved successfully.
Low Battery alert triggered for drone DRN-101.
Communication Lost alert triggered in North Region.
ERROR: Telemetry ingestion failed for drone DRN-205.
```

## How Logs Are Used
With ELK, SkyNetX teams can:

- search drone-specific incidents
- trace failed operations
- investigate emergency response events
- review approval activity
- support operational audits during demonstrations

## Local Demo Flow
1. Start ELK services:
   ```bash
   docker-compose -f logging/docker-compose-elk.yml up -d
   ```
2. Open Kibana:
   ```text
   http://localhost:5601
   ```
3. Configure Filebeat or send sample logs into Logstash for demonstration.

This setup is intentionally simple and meant for local college use, not production.
