import os
import boto3
from botocore.exceptions import ClientError

def connect_to_s3():
    ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    s3 = boto3.resource('s3', region_name='ap-south-1', 
        aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    return s3

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    s3 = connect_to_s3()

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return False
    return True