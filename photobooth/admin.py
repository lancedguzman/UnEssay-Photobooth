from django.contrib import admin
from .models import PhotoSession

class PhotoSessionAdmin(admin.ModelAdmin):
    """Admin interface for PhotoSession model."""
    list_display = ('id', 'session_type', 'created_at', 'user_message')
    list_filter = ('session_type', 'created_at')
    search_fields = ('id', 'user_message')
    readonly_fields = ('created_at',)

admin.site.register(PhotoSession, PhotoSessionAdmin)
