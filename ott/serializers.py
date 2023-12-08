# yourapp/serializers.py
from rest_framework import serializers
from .models import Ott

class UploadedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ott
        fields = '__all__'
