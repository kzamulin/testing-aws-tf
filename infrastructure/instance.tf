resource "aws_instance" "test" {
  ami                  = data.aws_ami.instance.id
  instance_type        = "t3.micro"
  iam_instance_profile = aws_iam_instance_profile.test_profile.name
  security_groups      = [aws_security_group.allow_ssh.name]
  key_name             = "kzamulin"

  user_data = "${file("../scripts/user_data.sh")}"

  tags = {
    Name = "kzamulin-test"
  }
}

resource "aws_iam_instance_profile" "test_profile" {
  name = "test_profile"
  role = aws_iam_role.role.name
}