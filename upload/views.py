import boto3
from rest_framework.views import APIView
from rest_framework.response import Response

from iravi_backend import settings
from .serializer import FileUploadSerializer


class FileUploadView(APIView):
    serializer_class = FileUploadSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            file_name = file.name
            folder_path = 'profile/'
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
                return Response({'url': url})
            except Exception as e:
                return Response({'error': f"Error uploading file: {e}"}, status=500)
        else:
            return Response({'error': serializer.errors}, status=400)
