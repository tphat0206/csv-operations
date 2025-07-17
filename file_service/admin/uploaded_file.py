from django.contrib import admin


class UploadedFileAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'uploaded_by',
        'created_at',
        'file'
    )

    search_fields = ('uuid',)
