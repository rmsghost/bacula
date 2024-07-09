terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.57.0"
    }
  }

    backend "s3" {
      #consulte o arquivo backend.tfvars e mude as variáveis
  }
}

provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "./modules/vpc"
}

module "ec2" {
  source = "./modules/ec2"
  #INSTANCETYPE = "t2.medium"
  SUBNET_ID = module.vpc.SUBNET_ID
  SG_ID  = module.vpc.SG_ID
}

