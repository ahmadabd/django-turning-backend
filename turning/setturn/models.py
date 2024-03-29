from django.db import models
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Create your models here.
class Roles(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
# Signal for Roles table
@receiver(post_migrate, sender=None)
def add_default_roles(sender, **kwargs):
    roles = ['User', 'Admin']
    for role in roles:
        Roles.objects.get_or_create(name=role)

    
class UserRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.role.name


class Organizations(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class OrganizationCategory(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.organization.name + " - " + self.category.name  
    
class Charges(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()

    def __str__(self):
        return self.name + " - " + str(self.amount)
    
class OrganizationCharges(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    charge = models.ForeignKey(Charges, on_delete=models.CASCADE)

    def __str__(self):
        return self.organization.name + " - " + self.charge.name + " - " + str(self.charge.amount)
    
class Turns(models.Model):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name + " - " + str(self.start_time) + " - " + str(self.end_time)