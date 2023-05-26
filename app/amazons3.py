import os
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

def connect_to_s3():
    ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    s3 = boto3.client('s3', region_name='ap-south-1', 
        aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    return s3

def upload_file(file_name: str, file_location: Path, bucket: str, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    if object_name is None:
        object_name = file_name
    

    s3_client = connect_to_s3()
    file_path = file_location.joinpath(file_name)
    # Upload the file
    try:
        with open(file_path, 'rb') as f:
            s3_client.put_object(Bucket=bucket, Key=object_name, Body=f)
    except ClientError as e:
        return False
    return True