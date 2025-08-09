from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        validators = [
            UniqueTogetherValidator(
                queryset = MenuItem.objects.all(),
                fields = ['title', 'price']
            ),
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CartSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only = True)
    user_id = serializers.IntegerField(write_only = True)

    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'user_id', 'menuitem', 'menuitem_id', 'price', 'quantity']
        validators = [
            UniqueTogetherValidator(
                queryset = Cart.objects.all(),
                fields = ['user_id', 'menuitem_id']
            )
        ]
