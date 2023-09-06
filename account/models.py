from django.db import models
from django.utils import timezone

import uuid
import hashlib
from datetime import timedelta


# Create your models here.

class User(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, max_length=50, primary_key=True, editable=False, null=False)
    password = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50)
    comment = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return self.user_id
    

def in_30_days():
    return timezone.now() + timedelta(days=30)

class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    access_datetime = models.DateTimeField(default=in_30_days)
    
    def str(self):
        dt = timezone.localtime(self.access_datetime).strftime('%Y-%m-%d %H:%M:%S')
        return self.user.user_id + '(' + dt + ') - ' + self.token 
    
    def create(user: User):
        if AccessToken.objects.filter(user=user).exists():
            AccessToken.objects.filter(user=user).delete()
            
        dt = timezone.now()
        string = str(user.user_id) + user.password + dt.strftime('%Y-%m-%d %H:%M:%S')
        hash = hashlib.sha1(string.encode('utf-8')).hexdigest()
        token = AccessToken.objects.create(
            user=user,
            token=hash,
            access_datetime=dt
        )
        return token