from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'password', 'nickname','comment', 'email']
        extra_kwargs = {'password': {'write_only': True}}
        
        def create(self, validated_data):
            user = User.objects.create_user(
                user_id=validated_data['user_id'],
                password=make_password(validated_data['password']),
                nickname=validated_data['nickname'],
                comment=validated_data['comment'],
                email= validated_data['email'],
            )
            return user