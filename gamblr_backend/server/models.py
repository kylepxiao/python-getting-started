from django.db import models
from rest_framework import serializers
from jsonfield import JSONField

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name

class JSON(models.Model):
    json = JSONField()