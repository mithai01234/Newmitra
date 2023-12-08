from rest_framework import serializers
from .models import Statusapp
from django.utils import timezone
import pytz
class StatusappSerializer(serializers.ModelSerializer):
    uploaded_date = serializers.SerializerMethodField()
    uploaded_time = serializers.SerializerMethodField()
    class Meta:
        model = Statusapp
        fields = '__all__'

    def get_uploaded_date(self, obj):
        # Convert to Indian time zone and return the date part
        indian_time = timezone.localtime(obj.uploaded_at, pytz.timezone('Asia/Kolkata'))
        return indian_time.date()

    def get_uploaded_time(self, obj):
        # Convert to Indian time zone and return the time part in 24-hour format
        indian_time = timezone.localtime(obj.uploaded_at, pytz.timezone('Asia/Kolkata'))
        return indian_time.strftime('%H:%M')