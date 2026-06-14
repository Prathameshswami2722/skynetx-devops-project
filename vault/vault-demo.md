# Vault Demo Commands for SkyNetX

## Start Vault in Dev Mode
```bash
vault server -dev
```

## Set Vault Address
```bash
export VAULT_ADDR='http://127.0.0.1:8200'
```

## Login with Dev Token
Use the root token shown in the Vault dev mode terminal:

```bash
vault login <root-token>
```

## Enable KV Secrets Engine
```bash
vault secrets enable -path=secret kv-v2
```

## Write Demo Secrets
```bash
vault kv put secret/skynetx/app \
  ADMIN_PASSWORD=admin123 \
  API_SECRET_KEY=skynetx-api-key-123 \
  DATABASE_PASSWORD=db-pass-demo \
  JWT_SECRET=jwt-secret-demo
```

## Read Demo Secrets
```bash
vault kv get secret/skynetx/app
```

## Apply SkyNetX Policy
```bash
vault policy write skynetx-policy vault/vault-policy.hcl
```
