from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class FileModel(models.Model):
    file = models.FileField(upload_to='files/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    upload_date = models.DateTimeField(auto_now_add=True)
    secure_url = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return str(self.file)