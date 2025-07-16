from django.db import models
from django.utils import timezone

from account.models import BaseModel

def upload_to(_instance, file_name):
    now = timezone.now()
    return f'uploads/{now.strftime("%Y")}/{now.strftime("%m")}/{file_name}'

class UploadedFile(BaseModel):
    file = models.FileField(upload_to=upload_to)
    name = models.CharField(max_length=255, blank=True, null=True)
    uploaded_by = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.name and self.file:
            self.name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else self.file.name