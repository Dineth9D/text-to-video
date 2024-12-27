import os
from tempfile import NamedTemporaryFile

import boto3
from botocore.exceptions import NoCredentialsError
from decouple import config


AWS_ACCESS_KEY = config("AWS_ACCESS_KEY")
AWS_SECRET_KEY = config("AWS_SECRET_KEY")
BUCKET_NAME = config("BUCKET_NAME")

def upload_to_s3(file_path, object_name=None):
    """
    Uploads a file to an S3 bucket and returns the file's URL.
    
    :param file_path: Path to the file to upload
    :param object_name: S3 object name. If not specified, file_path is used
    :return: URL of the uploaded file
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    
    try:
        s3_client.upload_file(file_path, BUCKET_NAME, object_name)
        
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_name}"
        return file_url
    
    except FileNotFoundError:
        print("The file was not found.")
        return None
    except NoCredentialsError:
        print("Credentials not available.")
        return None


def upload_verified_image_to_s3(image_content, object_name):
    """
    Uploads verified image content to an S3 bucket and returns the file's URL.
    
    :param image_content: Content of the image to upload
    :param object_name: S3 object name
    :return: URL of the uploaded file
    """
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(image_content)
        temp_file_path = temp_file.name
    
    try:
        file_url = upload_to_s3(temp_file_path, object_name)
        return file_url
    finally:
        os.remove(temp_file_path)