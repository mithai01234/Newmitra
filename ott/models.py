# yourapp/models.py
from django.db import models
from django.utils import timezone

class Ott(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

