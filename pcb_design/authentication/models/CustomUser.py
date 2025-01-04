from django.contrib.auth.models import AbstractUser
from .CustomUserManager import CustomUserManager
from django.db import models
class CustomUser(AbstractUser):
    # ROLE_CHOICES = [
    #     ('Admin', 'Admin'),
    #     ('CADesigner', 'CADesigner'),
    #     ('Approver', 'Approver'),
    #     ('Verifier', 'Verifier'),
    # ]    
    username = None
    email = models.EmailField(unique=True)
    # role = models.CharField(ROLE_CHOICES,max_length=100,default='CADesigner')
    
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
