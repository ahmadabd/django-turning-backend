from django.urls import path
from . import views

urlpatterns = [
    path('organizations', views.OrganizationsView.as_view(), name="organizations"),
]
