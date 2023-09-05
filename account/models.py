from django.db import models
import uuid

# Create your models here.

class User(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, max_length=50, primary_key=True, editable=False, null=False)
    password = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50)
    comment = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    
    def __str__(self) -> str:
        return self.user_id
    