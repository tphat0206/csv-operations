import logging
import os

from django.core.files.base import ContentFile

from file_service.models import FileOperation
from file_service.services import DeduplicatedCsvExec, UniqueCsvExec, FilterCsvExec

logger = logging.getLogger(__name__)


class FileOperationService:
    MAP_FILE_OPERATION_EXECUTOR = {
        FileOperation.FileOperationType.DEDUP: DeduplicatedCsvExec,
        FileOperation.FileOperationType.UNIQUE: UniqueCsvExec,
        FileOperation.FileOperationType.FILTER: FilterCsvExec,
    }

    def __init__(self, file_operation: FileOperation, celery_task_id: str):
        self.file_operation = file_operation
        self.operation_type = self.file_operation.type
        self.file = self.file_operation.file
        self.parameters = self.file_operation.parameters
        self.celery_task_id = celery_task_id

    def exec(self):
        try:
            self.file_operation.status = 'processing'
            self.file_operation.celery_task_id = self.celery_task_id
            self.file_operation.save(update_fields=['status', 'celery_task_id'])

            df = self.MAP_FILE_OPERATION_EXECUTOR[self.operation_type](self.file.file.path, self.parameters).exec()

            output_buffer = df.to_csv(index=False)

            content_file = ContentFile(output_buffer.encode('utf-8'))

            self.file_operation.processed_file.save(self._get_file_name, content_file, save=False)
            self.file_operation.status = 'completed'
            self.file_operation.error_message = None
            self.file_operation.save()

            logger.info(f"File operation {self.file_operation.type} completed for file_id: {self.file.uuid}")

        except Exception as e:
            logger.error(f"Error during CSV {self.file_operation.type} for file_id {self.file.uuid}: {e}",
                         exc_info=True)
            self.file_operation.status = 'failed'
            self.file_operation.error_message = str(e)
            self.file_operation.save(update_fields=['status', 'error_message'])


    @property
    def _get_file_name(self):
        base_name = os.path.basename(self.file.file.name)
        original_name, original_ext = os.path.splitext(base_name)
        processed_file_name = f"{original_name}_{self.operation_type}{original_ext}"
        return processed_file_name
