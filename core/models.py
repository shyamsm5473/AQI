import uuid
import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class PasswordResetOTP(models.Model):
    """6-digit OTP for password reset, valid for 10 minutes, single-use."""
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_otps')
    otp        = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)

    @classmethod
    def generate_for(cls, user):
        """Invalidate old OTPs and create a fresh one."""
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        code = str(random.randint(100000, 999999))
        return cls.objects.create(user=user, otp=code)

    def is_valid(self):
        """OTP must be unused and less than 10 minutes old."""
        return (not self.is_used) and (timezone.now() - self.created_at < timedelta(minutes=10))

    def __str__(self):
        return f"OTP({self.user.username}, used={self.is_used})"
