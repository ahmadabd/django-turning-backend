from django.urls import path
from .views import RegisterUserAPIView, LoginView, LogoutView

urlpatterns = [
    path('register', RegisterUserAPIView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
