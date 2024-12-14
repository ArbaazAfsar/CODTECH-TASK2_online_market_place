from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
   
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Customer_profile' )
    phone= models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name