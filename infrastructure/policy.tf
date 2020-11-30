resource "aws_iam_policy" "policy" {
  name        = "access-test-bucket-rw"
  path        = "/"
  description = "Policy to access my test s3 bucket"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AccessRWMyTestBucketWithPrefix",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::${var.s3_bucket_name}/${var.s3_bucket_prefix}/*",
                "arn:aws:s3:::${var.s3_bucket_name}"
            ]
        }
    ]
}
EOF
}