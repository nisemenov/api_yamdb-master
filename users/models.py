from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserBio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    bio = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        if self.user.is_superuser:
            self.role = 'admin'
        elif self.user.is_staff:
            self.role = 'moderator'
        else:
            self.role = 'user'
        self.email = self.user.email
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name
        super(UserBio, self).save(*args, **kwargs)
