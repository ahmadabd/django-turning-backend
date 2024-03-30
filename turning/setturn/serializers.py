from rest_framework import serializers
from .models import Organizations, Category, OrganizationCategory

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizations
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class OrganizationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationCategory
        fields = "__all__"