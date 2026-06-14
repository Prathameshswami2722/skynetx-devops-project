path "secret/data/skynetx/*" {
  capabilities = ["create", "read", "update", "list"]
}

path "secret/metadata/skynetx/*" {
  capabilities = ["list", "read"]
}
