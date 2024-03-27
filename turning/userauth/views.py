from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import login, logout
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)
    
class RegisterUserAPIView(CSRFExemptMixin, APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginView(CSRFExemptMixin, APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutView(CSRFExemptMixin, APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=200)
