from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrganizationSerializer
from .models import Organizations, UserRole, Roles
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass

@authentication_classes([CsrfExemptSessionAuthentication])
class OrganizationsView(APIView):
    permission_classes = (IsAuthenticated,)
    
    @csrf_exempt
    def post(self, request):
        userRole = UserRole.objects.get(user = request.user)
        if userRole.role.name != "Admin":
            return Response({'error': 'Admin can create organization'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['admin'] = request.user.id 
        serializer = OrganizationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        organizations = Organizations.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)