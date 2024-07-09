output "EC2-IP" {
    value = aws_instance.EC2DOCKER.public_ip
}

output "EC2-DNS" {
    value = aws_instance.EC2DOCKER.public_dns
}