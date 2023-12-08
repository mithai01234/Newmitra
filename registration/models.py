import phonenumbers
from django.utils.text import slugify
from phonenumbers.phonenumberutil import PhoneNumberFormat
from decimal import Decimal
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, name=None, referral_code=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number field must be set')
        user = self.model(phone_number=phone_number, name=name, referral_code=referral_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, name=None, referral_code=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, name, referral_code, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id= models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True)  # You can adjust the max_length as needed.
    name = models.CharField(max_length=255)
    bio=models.CharField(max_length=255,default='')
    profile_photo=models.ImageField(upload_to='videos/', null=True, blank=True)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store the password as a hash.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True)
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='users_blocked_by')
    username_code = models.CharField(unique=True,max_length=15, blank=True, null=True)
    status = models.IntegerField(default=1)
    email = models.EmailField(unique=True)
    slug = models.CharField(max_length=15, blank=True,unique=True, null=True)
    objects = CustomUserManager()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    level = models.PositiveIntegerField(default=1)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def update_total_amount(self, amount):
        self.total_amount += Decimal(amount)
        self.save()

    def save(self, *args, **kwargs):
        if not self.username_code:
            self.username_code = f"{self.name[:4]}_{random.randint(1000, 9999)}"
        if not self.slug:
            self.slug = f"{random.randint(1000, 9999)}"

        super(CustomUser, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} '

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_value = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user.name} OTP: {self.otp_value}'

class TableJoining(models.Model):
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referral_rewards_received')
    sponser_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referral_rewards_given')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Reward from {self.sponser_id} to {self.uid}'

    class Meta:
        verbose_name_plural = 'TableJoining'

# Usage example:
# Assuming you have a registered user with the username 'new_user' and a referral code 'referrer_code'
class Joining(models.Model):
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sponser_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sponsored_users')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.99)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateField(auto_now_add=True)

class Reward(models.Model):
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sponser_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sponsored_rewards')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateField(auto_now_add=True)


