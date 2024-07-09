terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.57.0"
    }
  }
  #Coloque aqui o bucket e o arquivo de .tfstate
  backend "s3" {
    bucket = "nome_do_bucket"
    key    = "nome_do_arquivo"
    region = "us-east-1"
  }
}


#Usando variáveis de ambiente - Para rodar em ambiente local
# export AWS_ACCESS_KEY_ID="anaccesskey"
# export AWS_SECRET_ACCESS_KEY="asecretkey"
# export AWS_REGION="us-west-2"
provider "aws" {
  region = "us-east-1"
}

##VPC##
resource "aws_vpc" "STACKOBSERVABILITY" {
  cidr_block           = "192.168.0.0/26"
  enable_dns_hostnames = "true"
  enable_dns_support   = "true"
  instance_tenancy     = "default"

  tags = {
    Name = "STACKOBSERVABILITY"
  }
}

##subnet##
resource "aws_subnet" "SUB_PUB" {
  vpc_id            = aws_vpc.STACKOBSERVABILITY.id
  cidr_block        = "192.168.0.0/27"
  availability_zone = "us-east-1c"
}

##SECURITY GROUPS##
resource "aws_security_group" "SG-EC2" {
  name        = "EC2-GROUP"
  description = "Security group para EC2"
  vpc_id      = aws_vpc.STACKOBSERVABILITY.id

  tags = {
    Name = "SG-EC2"
  }
}

resource "aws_vpc_security_group_ingress_rule" "any" {
  security_group_id = aws_security_group.SG-EC2.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = "0"
  to_port           = "0"
  ip_protocol       = "tcp"
}
resource "aws_vpc_security_group_ingress_rule" "SSH" {
  security_group_id = aws_security_group.SG-EC2.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = "22"
  to_port           = "22"
  ip_protocol       = "All"
}

resource "aws_vpc_security_group_egress_rule" "any" {
  security_group_id = aws_security_group.SG-EC2.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = "0"
  to_port           = "0"
  ip_protocol       = "All"
}

resource "aws_internet_gateway" "GW" {
  vpc_id = aws_vpc.STACKOBSERVABILITY.id

  tags = {
    Name = "GW"
  }
}

#resource "aws_internet_gateway_attachment" "GWATTACH" {
#  internet_gateway_id = aws_internet_gateway.GW.id
#  vpc_id = aws_vpc.STACKOBSERVABILITY.id
#}

resource "aws_route_table" "RT-OBSERVABILITY" {
  vpc_id = aws_vpc.STACKOBSERVABILITY.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.GW.id
  }

  tags = {
    Name = "RT-OBSERVABILITY"
  }
}

resource "aws_route_table_association" "RT-ASSOC" {
  subnet_id      = aws_subnet.SUB_PUB.id
  route_table_id = aws_route_table.RT-OBSERVABILITY.id
}


resource "aws_instance" "EC2DOCKER" {
  ami                         = "ami-0bb84b8ffd87024d8"
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.SUB_PUB.id
  key_name                    = "DEVOPS"
  associate_public_ip_address = "true"
  vpc_security_group_ids      = [aws_security_group.SG-EC2.id]
  user_data                   = file("script.sh")

} #end of file


output "infoEC2" {
  value = aws_instance.EC2DOCKER.public_ip
}

