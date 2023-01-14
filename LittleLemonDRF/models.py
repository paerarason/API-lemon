from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self)-> str:
        return self.title

  
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self)-> str:
        return self.title

class Orders(models.Model):
    products=models.ManyToManyField(MenuItem,related_name="ORDER_products")
    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="ordered_customer")
    delivery_crew=models.ForeignKey(User,on_delete=models.PROTECT,related_name="delivery_crew",blank=True)
    delivery_status=models.BooleanField(default=False)
    def __str__(self):
        return self.customer.username

class DeliveryProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="deliverycrew")
    availability_status=models.BooleanField(default=True)
    orders=models.ManyToManyField(Orders,related_name="his_orders",blank=True)

class Cart(models.Model):
    menu=models.ManyToManyField(MenuItem,related_name="order_menu")
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username 
class orders_places(models.Model):
    order=models.ManyToManyField(Orders,related_name="OUT_FOR",blank=True)
