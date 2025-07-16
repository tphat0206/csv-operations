import logging

from celery import shared_task

from file_service.models import FileOperation
from file_service.services import FileOperationService

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def file_operation_task(self, file_operation_uuid):
    try:
        file_operation_instance = FileOperation.objects.get(uuid=file_operation_uuid)
        FileOperationService(file_operation_instance, self.request.id).exec()
    except FileOperation.DoesNotExist:
        logger.error(f"File operation with id {file_operation_uuid} not found.")
