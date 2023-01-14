from rest_framework import serializers
from .models import MenuItem, Category,Cart,Orders
from decimal import Decimal
from django.contrib.auth.models import User
class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']
class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    price_after_gst=serializers.SerializerMethodField(method_name='gst')
    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory','category','category_id','price_after_gst']
    def gst(self,product:MenuItem):
        return product.price*Decimal(1.18)

class CartSerializer(serializers.ModelSerializer):
    menu=MenuItemSerializer(many=True,read_only=True)
    class Meta:
        model=Cart
        fields=['id','menu']

class OrderSerializer(serializers.ModelSerializer):
 delivery=CurrentUserSerializer(read_only=True)
 product=MenuItemSerializer(many=True,read_only=True)
 customer=CurrentUserSerializer(read_only=True)
 class Meta:
    model=Orders
    fields=['id','customer','product','delivery','delivery_status']