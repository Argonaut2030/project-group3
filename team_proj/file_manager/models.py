from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def user_directory_path(instance, filename):
    folder_mapping = {
        'jpg': 'images', 'jpeg': 'images', 'png': 'images', 'gif': 'images',
        'mp4': 'videos', 'mov': 'videos', 'avi': 'videos',
        'mp3': 'audio', 'wav': 'audio', 'aac': 'audio',
    }
    ext = filename.split('.')[-1].lower()
    folder = folder_mapping.get(ext, 'documents')
    return f"user_{instance.user.id}/{folder}/{filename}"

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)


