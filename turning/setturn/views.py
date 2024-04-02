from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrganizationSerializer, CategorySerializer, OrganizationCategorySerializer
from .models import Organizations, UserRole, Category, OrganizationCategory
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import SessionAuthentication
from django.db.models import Q

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
    
@authentication_classes([CsrfExemptSessionAuthentication])
class CategoriesView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        userRole = UserRole.objects.get(user = request.user)
        if userRole.role.name != "Admin":
            return Response({'error': 'Admin can create category'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

@authentication_classes([CsrfExemptSessionAuthentication])
class OrganizationCategoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        userRole = UserRole.objects.get(user = request.user)
        if userRole.role.name != "Admin":
            return Response({'error': 'Admin can create category'}, status=status.HTTP_400_BAD_REQUEST)

        organization = Organizations.objects.get(id=id)
        data = request.data.copy()
        data['organization'] = id
        serializer = OrganizationCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save(organization=organization)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        organization = Organizations.objects.get(id=id)
        organizationCategory = OrganizationCategory.objects.filter(organization=organization)
        if not organizationCategory.exists():
            return Response({'error': 'Organization not found or dosent have category'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(organizationCategory.get().category)
        return Response(serializer.data)
    
class SearchOrganizationsView(APIView):

    def get(self, request):
        organizations = Organizations.objects.filter(Q(name__icontains = request.GET.get("search")) | 
                                                     Q(organizationcategory__category__name = request.GET.get("search")))

        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)
    
class GETCategoryOrganizations(APIView):
    def get(self, request, id):
        organizations = Organizations.objects.filter(organizationcategory__category__id = id)

        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)