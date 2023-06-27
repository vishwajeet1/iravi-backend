import boto3
import threading
from iravi_backend import settings
from upload.serializer import FileUploadSerializer


def uploadFileToS3Bucket(file, folder_path):
    serializer = FileUploadSerializer(data=file)
    if serializer.is_valid():
        file = serializer.validated_data['file']
        file_name = file.name
        s3_key = f"{folder_path}{file_name}"
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME
                          )
        try:
            s3_response = s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, s3_key, ExtraArgs={
                "ACL": "public-read"
            })
            url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"
            return {'success': True, 'url': url}
        except Exception as e:
            return {'success': False, 'error': f"Error uploading file: {e}"}
    else:
        return {'success': False, 'error': serializer.errors}