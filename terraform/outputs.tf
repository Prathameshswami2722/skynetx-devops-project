output "vpc_id" {
  description = "ID of the sample SkyNetX VPC."
  value       = aws_vpc.skynetx_vpc.id
}

output "subnet_id" {
  description = "ID of the sample SkyNetX subnet."
  value       = aws_subnet.skynetx_public_subnet.id
}

output "security_group_id" {
  description = "ID of the sample SkyNetX security group."
  value       = aws_security_group.skynetx_sg.id
}

output "instance_public_ip" {
  description = "Public IP of the demo EC2 instance."
  value       = aws_instance.skynetx_demo_instance.public_ip
}
