from django.db import models
from rest_framework import serializers

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name