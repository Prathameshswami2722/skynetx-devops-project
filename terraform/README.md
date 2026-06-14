# SkyNetX Terraform Support

This folder contains basic Terraform files for demonstrating Infrastructure as Code in the SkyNetX DevOps project.

## Purpose
Terraform allows infrastructure to be defined in code so it can be planned, reviewed, created, updated, and destroyed in a repeatable way. For SkyNetX, Terraform represents the infrastructure automation part of the larger DevOps ecosystem.

## Included Concepts
The files include example placeholders for:

- VPC
- subnet
- security group
- EC2 instance
- Kubernetes cluster concept for future extension

## Important Note
These files are for college demonstration. They use simple example resources and comments. Review AMI IDs, region settings, and costs before applying in a real AWS account.

## Commands
Initialize Terraform:

```bash
terraform init
```

Validate configuration:

```bash
terraform validate
```

Create an execution plan:

```bash
terraform plan
```

Apply the configuration:

```bash
terraform apply
```

Destroy the resources:

```bash
terraform destroy
```

## SkyNetX Relevance
In the SkyNetX case study, Terraform helps standardize infrastructure provisioning, reduce deployment inconsistency, and support scalable DevOps operations across environments.
