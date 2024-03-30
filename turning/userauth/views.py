from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import login, logout
from rest_framework import status
from setturn.models import UserRole, Roles
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass

@authentication_classes([CsrfExemptSessionAuthentication])
class RegisterUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if request._data["admin"] == 1:
                userRole = Roles.objects.get(name="Admin")    
            else:
                userRole = Roles.objects.get(name="User")
            userRole = UserRole.objects.create(user=user, role=userRole)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@authentication_classes([CsrfExemptSessionAuthentication])
class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({"message": "Successfully logged in"}, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=200)
