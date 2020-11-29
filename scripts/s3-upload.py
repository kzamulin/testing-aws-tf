import sys
import os
import glob
import boto3
import json
import time
from datetime import datetime, timedelta

# Simple script that can create files, upload them to specified bucket and prefix and perform local cleanup and cleanup on s3
# Usage:
# -----
# python s3-upload.py upload <bucket name> <prefix name>            - creates 10 files with timestamp with 2 second interval and uploads each to specified bucket and prefix
# python s3-upload.py cleanup                                       - to cleanup local directory from created files
# python s3-upload.py s3cleanup <bucket name> <prefix name> full    - to cleanup all files in specified s3 bucket and prefix
# python s3-upload.py s3cleanup <bucket name> <prefix name> leave3  - cleans up all files in specified s3 bucket and prefix except the 3 ones with most recent timestamp

# Just simple cleanup
if sys.argv[1] == "cleanup":
    print("Cleaning up...")
    for file_name in glob.glob('test*.ext'):
        os.remove(file_name)
        print("Removed file " + file_name)

# Cleanup s3 bucket files by name and prefix
if sys.argv[1] == "s3cleanup":
    bucket_name = sys.argv[2]
    prefix_name = sys.argv[3]
    cl_type = sys.argv[4]
    s3_client = boto3.client('s3')

    # Full or like in task (delete all except three the earlier)
    if cl_type == "full":
        for key in s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix_name)['Contents']:
            print("Deleting key from " + bucket_name + ": " + key['Key'])
            response = s3_client.delete_object(Bucket=bucket_name, Key=key['Key'])
            print(response)
    elif cl_type == "leave3":
        files = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix_name)['Contents']
        files.sort(reverse=True,key = lambda x:x['LastModified'])
        for key_num in range(len(files)):
            key = files[key_num]
            if key_num < 3:
                print("Key: " + key['Key'] + ", timestamp: " + str(key['LastModified']) + "(Remained)")
            else:
                response = s3_client.delete_object(Bucket=bucket_name, Key=key['Key'])
                print("Key: " + key['Key'] + ", timestamp: " + str(key['LastModified']) + "(Deleted)")
                print(response)


# Creating files and uploading to s3 bucket
if sys.argv[1] == "upload":
  bucket_name = sys.argv[2]
  prefix_name = sys.argv[3]
  s3_client = boto3.client('s3')

  for file_num in range(10):
      # If number is odd, then create it with one hour older timestamp
      file_name="test_file_" + str(file_num) + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ".ext"
      file = open(file_name,"w")
      file.write("Hello, file, " + file_name + "!")
      file.close()

      # Write file to provided s3 bucket and prefix
      response = s3_client.put_object(Body=open(file_name, 'rb'), Bucket=bucket_name, Key=prefix_name + '/' + file_name)
      print(response)

      #sleep just have different ts
      time.sleep(2)