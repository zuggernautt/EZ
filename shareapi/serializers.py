from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FileModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ('id', 'user', 'file', 'file_type', 'upload_date', 'secure_url')
