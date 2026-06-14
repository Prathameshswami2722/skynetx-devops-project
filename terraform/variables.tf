variable "aws_region" {
  description = "AWS region for the SkyNetX demo infrastructure."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name prefix used for sample SkyNetX resources."
  type        = string
  default     = "skynetx"
}
