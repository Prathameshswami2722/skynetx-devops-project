locals {
  common_tags = {
    Project     = "SkyNetX"
    Environment = "Demo"
    ManagedBy   = "Terraform"
  }
}

# This file is intentionally lightweight for a college demonstration.
# It shows how SkyNetX infrastructure can be modeled as code without
# creating expensive resources by default.

resource "aws_vpc" "skynetx_vpc" {
  cidr_block           = "10.10.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-vpc"
  })
}

resource "aws_subnet" "skynetx_public_subnet" {
  vpc_id                  = aws_vpc.skynetx_vpc.id
  cidr_block              = "10.10.1.0/24"
  map_public_ip_on_launch = true

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-public-subnet"
  })
}

resource "aws_security_group" "skynetx_sg" {
  name        = "${var.project_name}-sg"
  description = "Sample security group for SkyNetX demo services"
  vpc_id      = aws_vpc.skynetx_vpc.id

  ingress {
    description = "HTTP access"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Flask demo access"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-security-group"
  })
}

# Placeholder EC2 instance to represent a demo application node.
# In an actual implementation, SkyNetX could use managed Kubernetes,
# autoscaling groups, and separate database or monitoring layers.
resource "aws_instance" "skynetx_demo_instance" {
  ami                    = "ami-0f58b397bc5c1f2e8"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.skynetx_public_subnet.id
  vpc_security_group_ids = [aws_security_group.skynetx_sg.id]

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-demo-instance"
  })
}

# Concept note:
# A future SkyNetX version can replace the EC2 placeholder with:
# - managed Kubernetes cluster
# - worker nodes
# - load balancer
# - managed database
# - monitoring stack
