# SkyNetX Disaster Recovery Plan

## Purpose
This disaster recovery plan helps the SkyNetX platform maintain availability and recover from failures affecting autonomous drone traffic operations.

## RTO and RPO
- RTO (Recovery Time Objective): the target time to restore service after a failure.
- RPO (Recovery Point Objective): the acceptable amount of data loss measured in time.

For a college demonstration:
- Target RTO: 15 to 60 minutes depending on incident type
- Target RPO: 5 to 15 minutes for operational data and backups

## Recovery Scenarios
### Pod Failure
- Kubernetes restarts failed pods automatically.
- Verify status with:
  ```bash
  kubectl get pods -n skynetx
  ```

### Node Failure
- Reschedule workloads on healthy nodes if available.
- Review cluster events:
  ```bash
  kubectl get events -n skynetx
  ```

### Bad Deployment
- Roll back to the last working version:
  ```bash
  kubectl rollout undo deployment/skynetx-app -n skynetx
  ```

### Traffic Spike
- Scale the deployment manually:
  ```bash
  kubectl scale deployment skynetx-app --replicas=5 -n skynetx
  ```
- HPA can also help scale automatically.

### Region Failure
- Restore service in a secondary cluster or backup region in a future expanded design.
- Use backups of manifests, container images, and database exports.

### Database Failure
- Restore the latest backup and validate data consistency.
- Reconnect the application and verify dashboard and telemetry functions.

### Secret Compromise
- Rotate all affected credentials.
- Replace Kubernetes secrets and update Vault entries.
- Restart pods after secret update.

### Cybersecurity Incident
- Isolate impacted services.
- inspect logs, events, and access history.
- rotate secrets and credentials.
- redeploy trusted container images.
- document incident timeline and recovery actions.
