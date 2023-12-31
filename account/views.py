from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import User, AccessToken
from .serializers import RegisterSerializer, LoginSerializer

import hashlib

# Create your views here.
class RegisterView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # リクエストのパスワードと確認用パスワードが一致しているか確認
            if serializer.validated_data['password'] != request.data['password_confirmation']:
                return Response({'error': 2}, status=HTTP_400_BAD_REQUEST)
            try:
                serializer.validated_data['password'] = hashlib.sha256(serializer.validated_data['password'].encode()).hexdigest()
                # データベースに保存
                serializer.save()
            except:
                return Response({'error': 11}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.validated_data['email'])
            email = serializer.validated_data['email']
            token = AccessToken.create(user)
            return Response({'detail': "Login SUCCESS", 'token': token.token, 'error': 0}, status=HTTP_200_OK)
        return Response({'detail': "Login FAILED", 'error': 1}, status=HTTP_400_BAD_REQUEST)