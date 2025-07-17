from django.contrib import admin


class FileOperationAdmin(admin.ModelAdmin):
    list_display = (
        'file',
        'type',
        'status',
        'performed_by'
    )

    search_fields = ('uuid', 'file__name')
