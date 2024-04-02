from django.urls import path
from . import views

urlpatterns = [
    path('organizations', views.OrganizationsView.as_view(), name="organizations"),
    path('search-organizations', views.SearchOrganizationsView.as_view(), name="searchOrganizations"),
    path('categories', views.CategoriesView.as_view(), name="categories"),
    path('organization/category/<int:id>', views.OrganizationCategoryView.as_view(), name="organizationCategory"),
    path('organization/category/get/<int:id>', views.GETCategoryOrganizations.as_view(), name="GETCategoryOrganizations"),
]
