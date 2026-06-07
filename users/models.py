from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)