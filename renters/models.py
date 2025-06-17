from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.
User = get_user_model()

class profile(models.Model):

    r_or_c = [
        ('R',"Renter"),
        ('C', "Client"),
    ]

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    phone = models.IntegerField(max_length = 10)
    email = models.EmailField()
    renter_or_client = models.CharField(max_length=2 ,choices=r_or_c)

    def __str__(self):
        return self.user
    

class Item(models.Model):   
    AVAILABILITY_CHOICES = [
        ("IS", "In Stock"),
        ("OS","Out of Stock")
    ] 
    profile = models.ForeignKey(profile, on_delete = models.CASCADE)
    title = models.CharField(max_length = 99)
    slug = models.SlugField()
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add = True)
    description = models.TextField(max_length = 199)
    image = models.ImageField(upload_to="products/")
    availability = models.CharField(max_length = 2, choices = AVAILABILITY_CHOICES, default = "IS")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('renters:item_details',args=[self.slug])
    

class orderitem(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    ordered = models.BooleanField(default = False)

    def __str__(self):
        return self.item.title
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(orderitem)
    created_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_username()
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total
    
    def effective_price(self):
        shipping_price = 50
        total = self.get_total()
        effective_price = total + shipping_price
        return effective_price
