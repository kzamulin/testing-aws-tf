#! /bin/bash
yum install git -y
yum install python-boto3 -y
cd /home/ec2-user
git clone https://github.com/kzamulin/testing-aws-tf.git
chown -R ec2-user. /home/ec2-user/testing-aws-tf