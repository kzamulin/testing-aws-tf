variable "instance_ami_name" {
    default = "amzn2-ami-hvm-*-x86_64-gp2"
}

variable "instance_ami_owner" {
    default = "137112412989"
}

variable "s3_bucket_name" {
    default = "kzamulin-test"
}

variable "s3_bucket_prefix" {
    default = "test"
}