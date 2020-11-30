data "aws_ami" "instance" {
  most_recent = true

  filter {
    name   = "name"
    values = ["${var.instance_ami_name}"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["${var.instance_ami_owner}"]
}
