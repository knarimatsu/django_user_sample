from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from rest_framework import serializers
from .models import User, AccessToken
import hashlib


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
        
class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccessToken
        fields = ['email', 'password']
        

    email = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = hashlib.sha256(data.get('password').encode()).hexdigest()
        try:
            user = User.objects.get(email=email)
            re_password = user.password
            if email == user.email:        
                if password == re_password:
                    return data
                else:
                    raise serializers.ValidationError("ログイン失敗")
        except:
            raise serializers.ValidationError({'detail': "Login FAILED", 'error': 1}, HTTP_400_BAD_REQUEST)