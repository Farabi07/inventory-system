from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="+",null=True,blank=True
    )
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="+",null=True,blank=True
    )
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.replace(' ', '_').upper()
        super().save(*args, **kwargs)


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
