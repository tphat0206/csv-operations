import json
import logging

from rest_framework import serializers

from file_service.models import FileOperation, UploadedFile
from file_service.services import ReadProcessedCsv
from file_service.tasks import file_operation_task

logger = logging.getLogger(__name__)


class CreateFileOperationSerializer(serializers.ModelSerializer):
    column_name = serializers.CharField(write_only=True, required=False)
    filter_params = serializers.JSONField(write_only=True, required=False)
    type = serializers.CharField(write_only=True, required=True)
    file = serializers.PrimaryKeyRelatedField(queryset=UploadedFile.objects.all(), write_only=True, required=True)
    task_id = serializers.CharField(read_only=True, source='uuid')

    class Meta:
        model = FileOperation
        fields = [
            'task_id', 'file', 'column_name', 'filter_params',
            'type',
        ]

    def validate_file(self, file):
        if not self.context['request'].user.uploadedfile_set.filter(pk=file.uuid).exists():
            raise serializers.ValidationError('File does not exist.')
        return file

    def validate_type(self, type):
        if type not in FileOperation.FileOperationType.values:
            raise serializers.ValidationError('Invalid file operation type.')
        return type

    def create(self, validated_data):
        parameters = {}
        if validated_data['type'] == FileOperation.FileOperationType.DEDUP:
            pass
        elif validated_data['type'] == FileOperation.FileOperationType.UNIQUE:
            column_name = validated_data.pop('column_name')
            if not column_name:
                raise serializers.ValidationError('Missing parameter "column_name"')
            parameters = {'column_name': column_name}
        elif validated_data['type'] == FileOperation.FileOperationType.FILTER:
            filter_params = validated_data.pop('filter_params')
            if not filter_params:
                raise serializers.ValidationError('Missing parameter "filter_params"')
            elif not isinstance(filter_params, list):
                raise serializers.ValidationError('"filter_params" must be or list')
            parameters = filter_params

        validated_data['parameters'] = json.dumps(parameters)
        validated_data['performed_by'] = self.context.get('request').user
        file_operation = super(CreateFileOperationSerializer, self).create(validated_data)

        file_operation_task.delay(file_operation.uuid)

        return file_operation


class FileOperationSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField(required=False)
    error = serializers.CharField(source='error_message', required=False)
    task_id = serializers.CharField(source='uuid')

    class Meta:
        model = FileOperation
        fields = ['task_id', 'status', 'results', 'error']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return {key: value for key, value in ret.items() if value is not None}

    def get_results(self, obj):
        request = self.context.get('request')
        n_value = getattr(request, 'n_value', None)
        if obj.status == FileOperation.FileOperationStatus.SUCCEEDED:
            file_path = obj.file.file.path
            data = ReadProcessedCsv(file_path, n_value).exec()
            return {
                'data': data,
                'file_link': obj.processed_file.url,
            }
        return None
