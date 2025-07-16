from django.contrib import admin
from .models import UploadedFile, FileOperation

admin.site.register(UploadedFile)
admin.site.register(FileOperation)
