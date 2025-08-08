from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework.validators import UniqueTogetherValidator

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