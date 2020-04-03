from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import File, JSON


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

class JsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = JSON
        fields = "__all__"