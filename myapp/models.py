from django.db import models
from django.contrib.auth.models import User

class FileAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projectname = models.CharField(max_length=255)
    filename = models.CharField(max_length=255, unique=True)  # Ensures uniqueness per user
    remark = models.CharField(max_length=255)
    uploadfile = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f"{self.user.username} - {self.filename}"






