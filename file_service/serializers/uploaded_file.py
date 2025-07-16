from rest_framework import serializers

from file_service.models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFile
        fields = ['uuid', 'file', 'name', 'created_at', 'uploaded_by']
        read_only_fields = ['created_at', 'uploaded_by']

    def validate_file(self, file):
        if file.content_type != 'text/csv':
            raise serializers.ValidationError(
                'Invalid file format. Only CSV files are allowed.'
            )

        return file

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['uploaded_by'] = user
        uploaded_file = super(UploadedFileSerializer, self).create(validated_data)

        return uploaded_file