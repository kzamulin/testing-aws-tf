output "instance_fqdn" {
    value = aws_instance.test.public_dns
}

output "instance_fqdn_with_user" {
    value = "ec2-user@${aws_instance.test.public_dns}"
}