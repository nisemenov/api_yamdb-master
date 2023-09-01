from django.db import models
from django.contrib.auth.models import User


class UserBio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20)
    confirmation_code = models.CharField(max_length=8, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.user.is_superuser:
            self.role = 'admin'
        elif self.user.is_staff:
            self.role = 'moderator'
        else:
            self.role = 'user'
        super(UserBio, self).save(*args, **kwargs)
