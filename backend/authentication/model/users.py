from django.db import models
import os
from .base import TimeStampedModel
def user_image_path(instance,filename):
    email:str = instance.email
    return os.path.join(f'user_{email[:email.index('@')]}_{filename}')


class User(TimeStampedModel):
    """Model definition for User."""
    fname = models.CharField(max_length=30)
    lname = models.CharField(blank=True,null=True,max_length=30)
    email = models.EmailField(unique=True,db_index=True)
    hashed_password = models.CharField(max_length=72)
    photo = models.ImageField(blank=True,null=True,upload_to=user_image_path)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin'), ('creator', 'Creator')], default='user')
    is_verified = models.BooleanField(default=True)
    salt = models.CharField(max_length=29,default='')
    
    class Meta:
        """Meta definition for User."""

        verbose_name = 'User'
        verbose_name_plural = 'Users'

   
