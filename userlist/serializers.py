from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class CustomuSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'id','name', 'email', 'referral_code', 'profile_photo', 'bio')
