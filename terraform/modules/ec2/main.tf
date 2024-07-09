terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.57.0"
    }
  }
}

resource "aws_instance" "EC2DOCKER" {
  ami                         = "ami-0bb84b8ffd87024d8"
  instance_type               = var.INSTANCETYPE
  subnet_id                   = var.SUBNET_ID
  key_name                    = "DEVOPS"
  associate_public_ip_address = "true"
  vpc_security_group_ids      = [var.SG_ID]
  user_data                   = file("../src/script.sh")
}