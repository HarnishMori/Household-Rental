from django.db import models
from django.contrib.auth.models import User
from renters.models import orderitem, profile
# Create your models here.
    
class FinalOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()

class CnfOrder(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    profile = models.ForeignKey(profile, on_delete=models.CASCADE)
    final = models.ForeignKey(FinalOrder, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    ship_to_different_address = models.BooleanField(default=False)
    order_notes = models.TextField(blank=True)

    def __str__(self):
        return self.profile.user.username

class OrderDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    final = models.ForeignKey(FinalOrder, on_delete=models.CASCADE)
    orderitem = models.ForeignKey(orderitem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, max_length=99)
    subtotal = models.FloatField(default=0)

