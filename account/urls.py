from . import views
from django.urls import path, include

urlpatterns = [
     path('signup/', views.RegisterView.as_view(), name='user-signup')
]