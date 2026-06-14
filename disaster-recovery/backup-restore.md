# SkyNetX Backup and Restore Notes

## Backup Scope
Back up the following items regularly:

- application source code
- Docker and Kubernetes manifests
- Jenkins pipeline file
- monitoring, logging, Vault, and Terraform files
- SQLite database exports
- operational documentation

## Restore Steps
1. Restore project source from GitHub.
2. Rebuild the Docker image:
   ```bash
   docker build -t skynetx-app:1.0 .
   ```
3. Reapply Kubernetes manifests:
   ```bash
   kubectl apply -f kubernetes/
   ```
4. Restore database backup if needed.
5. Validate `/health`, dashboard access, and basic business flows.

## Validation Checklist
- app pods are running
- service is reachable
- Jenkins pipeline is available
- metrics are exposed
- secrets are restored securely
