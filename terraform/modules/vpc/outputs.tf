output "SUBNET_ID" {
    value = aws_subnet.SUB_PUB.id
}
output "SG_ID" {
    value = aws_security_group.SG-EC2.id
}