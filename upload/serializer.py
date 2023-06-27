from abc import ABC

from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        max_size = 100 * 1024  # 100 KB
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File size should not exceed {max_size} bytes.")
        if not value.name.lower().endswith(tuple(allowed_extensions)):
            raise serializers.ValidationError(
                f"File type not supported. Allowed types: {', '.join(allowed_extensions)}.")
        return value
