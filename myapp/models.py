from django.db import models
from django.contrib.auth.models import User

class FileAnalysis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the built-in User model
    projectname = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)
    uploadfile = models.FileField(upload_to='uploads/')  # Use FileField for file uploads

    def __str__(self):
        return self.filename






