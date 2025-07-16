from django.db import models
from django.utils import timezone

from account.models import BaseModel

def upload_to(_instance, file_name):
    now = timezone.now()
    return f'processed_files/{now.strftime("%Y")}/{now.strftime("%m")}/{now.strftime("%H%M%S")}_{file_name}'

class FileOperation(BaseModel):
    class FileOperationType(models.TextChoices):
        DEDUP = 'dedup'
        UNIQUE = 'unique'
        FILTER = 'filter'

    class FileOperationStatus(models.TextChoices):
        PENDING = 'pending'
        SUCCEEDED = 'succeeded'
        FAILED = 'failed'
        CANCELED = 'canceled'

    file = models.ForeignKey('file_service.UploadedFile', on_delete=models.CASCADE)
    type = models.CharField(choices=FileOperationType.choices, default=FileOperationType.DEDUP, max_length=50)
    status = models.CharField(choices=FileOperationStatus.choices, default=FileOperationStatus.PENDING, max_length=50)
    performed_by = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    celery_task_id = models.CharField(max_length=255, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    parameters = models.JSONField(blank=True, null=True)
    processed_file = models.FileField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return f'{self.file}_{self.type}'