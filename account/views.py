from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import RegisterSerializer

# Create your views here.
class RegisterView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        # print(request.data)
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            # リクエストのパスワードと確認用パスワードが一致しているか確認
            if serializer.validated_data['password'] != request.data['password_confirmation']:
                return Response({'error': 2}, status=HTTP_400_BAD_REQUEST)
            try:
                # データベースに保存
                serializer.save()
            except:
                print('データベース保存失敗')
                return Response({'error': 11}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    