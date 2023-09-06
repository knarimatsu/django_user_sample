from rest_framework import serializers
from .models import User



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'password', 'nickname','comment', 'email', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
                
        def create(self, validated_data):
            user = User.objects.create(
                user_id=validated_data['user_id'],
                password=validated_data['password'],
                nickname=validated_data['nickname'],
                comment=validated_data['comment'],
                email= validated_data['email'],
            )
            return user