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
    for file_name in glob.glob(directory + '/' file_name_prefix + '*.' + file_name_extension):
        os.remove(file_name)
        print("Removed file " + file_name)

# Cleanup s3 bucket files by name and prefix
def s3_cleanup(bucket_name,prefix_name,cl_type):
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
def create_files_and_upload_to_s3_bucket(bucket_name, prefix_name, number_of_files_to_create)
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
    parent_parser = argparse.ArgumentParser()
    child_parser = argparse.ArgumentParser(parents=[parent_parser])

    parent_parser.add_argument(
        "-c", 
        "--command",
        required=True,
        type=str,
        help="Specify command: \n * cleanup - for local directory files clean up \n * s3cleanup - for s3 specified bucket and prefix cleanup \n * upload - to create test files and upload them to specified s3 bucket and prefix"
    )

    child_parser.add_argument(
        "-b", 
        "--bucket",
        type=str,
        help="Specify bucket name to upload files to, or delete files from."
    )

    child_parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        help="Specify bucket prefix to upload files to, or delete files from"
    )

    child_parser.add_argument(
        "-o",
        "--option",
        default="leave3",
        type=str,
        help="Option to remove all files from s3 bucket, or leave three files with recent value."
    )


    if parent_parser.parse_args().c == "upload":
        create_files_and_upload_to_s3_bucket(child_parser.parse_args().b, child_parser.parse_args().p,10)
    elif parent_parser.parse_args().c == "cleanup":
        local_cleanup("test", "ext", os.path[0]+child_parser.parse_args().p)
    elif parent_parser.parse_args().c == "s3cleanup":
        s3_cleanup(child_parser.parse_args().b, child_parser.parse_args().p, child_parser.parse_args().o)

if __name__ == "__main__": main()