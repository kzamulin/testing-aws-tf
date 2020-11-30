# ----------------------------------------------------------------------------------------------------------------------------------------
# Simple script that can create files, upload them to specified bucket and prefix and perform local cleanup and cleanup on s3

import os
import argparse
import glob
import boto3
import json
import time
from datetime import datetime, timedelta

# Just simple cleanup
def local_cleanup(file_name_prefix, file_name_extension, directory):
    print("Cleaning up...")
    for file_name in glob.glob(directory + '/' + file_name_prefix + '*.' + file_name_extension):
        os.remove(file_name)
        print("Removed file " + file_name)

# Cleanup s3 bucket files by name and prefix
def s3_cleanup(bucket_name, prefix_name, cl_type):
    s3_client = boto3.client('s3')

    # Full or like in task (delete all except three the earlier)
    if cl_type:
        for key in s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix_name)['Contents']:
            print("Deleting key from " + bucket_name + ": " + key['Key'])
            response = s3_client.delete_object(Bucket=bucket_name, Key=key['Key'])
            print(response)
    else:
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
def create_files_and_upload_to_s3_bucket(bucket_name, prefix_name, number_of_files_to_create):
    s3_client = boto3.client('s3')

    test_files_directory = os.path[0] + prefix_name

    if not os.path.exists(test_files_directory):
        os.makedirs(test_files_directory)

    for file_num in range(number_of_files_to_create):
        # If number is odd, then create it with one hour older timestamp
        file_name="test_file_" + str(file_num) + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ".ext"
        file = open(test_files_directory + '/' + file_name,"w")
        file.write("Hello, file, " + file_name + "!")
        file.close()

        # Write file to provided s3 bucket and prefix
        response = s3_client.put_object(Body=open(test_files_directory + '/' + file_name, 'rb'), Bucket=bucket_name, Key=prefix_name + '/' + file_name)
        print(response)

        #sleep just have different ts
        time.sleep(2)

def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='commands')

    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help="local directory files clean up")
    cleanup_parser.add_argument("-d", "--directory", type=str, default="test", help="Which local directory to cleanup")

    # S3 bucket cleanup command

    s3cleanup_parser = subparsers.add_parser('s3cleanup_parser', help="Cleanup specified s3 bucket and prefix")
    s3cleanup_parser.add_argument("-b", "--bucket", type=str, help="Specify bucket name")
    s3cleanup_parser.add_argument("-p", "--prefix", type=str, help="Specify prefix name")
    s3cleanup_parser.add_argument("--full", help="Perform full cleanup of s3 bucket")

    # Upload command
    upload_parser = subparsers.add_parser('upload', help="Create test files and upload to s3 bucket")
    upload_parser.add_argument("-b","--bucket", type=str, help="Specify bucket name")
    upload_parser.add_argument("-p","--prefix", type=str, help="Specify prefix name")

    args = parser.parse_args()

    if args.upload:
        create_files_and_upload_to_s3_bucket(args.upload.bucket, args.upload.prefix, 10)
    elif args.cleanup:
        local_cleanup("test", "ext", os.path[0] + args.cleanup.directory)
    elif args.s3cleanup:
        s3_cleanup(args.s3cleanup.bucket, args.s3cleanup.prefix, args.s3cleanup.full)

if __name__ == "__main__": main()