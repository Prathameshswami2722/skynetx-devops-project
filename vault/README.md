# SkyNetX Vault Support

This folder contains simple secret-management documentation and policy examples for the SkyNetX DevOps project.

## Included Files
- `vault-policy.hcl`
- `vault-demo.md`

## Why Vault Matters for SkyNetX
SkyNetX handles operational and administrative information for a drone traffic management platform. Secrets such as admin passwords, API keys, database credentials, and JWT secrets should be managed securely.

## Secrets Used in Demo
- `ADMIN_PASSWORD`
- `API_SECRET_KEY`
- `DATABASE_PASSWORD`
- `JWT_SECRET`

## Why Secrets Should Not Be Stored in Unsafe Places
Secrets should not be stored directly in:

- GitHub repositories
- Dockerfiles
- Kubernetes YAML manifests in plain text
- Flask application source code

This is important because those locations can be copied, leaked, committed accidentally, or exposed to too many users and systems.

## Vault Role
Vault provides:

- centralized secret storage
- controlled secret access
- audit-friendly secret handling
- safer credential usage for future CI/CD and Kubernetes integration

## Local Demo
Use Vault dev mode for local demonstration. The commands are available in `vault-demo.md`.

This setup is intentionally simple for college use and can be extended later with Kubernetes authentication, dynamic secrets, and better access control.
