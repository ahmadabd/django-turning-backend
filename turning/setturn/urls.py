from django.urls import path
from . import views

urlpatterns = [
    path('organizations', views.OrganizationsView.as_view(), name="organizations"),
    path('categories', views.CategoriesView.as_view(), name="categories"),
    path('organization/category/<int:id>', views.OrganizationCategoryView.as_view(), name="organizationCategory"),
]
