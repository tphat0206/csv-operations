from django.contrib import admin

from file_service.admin.file_operation import FileOperationAdmin
from file_service.admin.uploaded_file import UploadedFileAdmin
from file_service.models import UploadedFile, FileOperation

admin.site.register(UploadedFile, UploadedFileAdmin)
admin.site.register(FileOperation, FileOperationAdmin)
