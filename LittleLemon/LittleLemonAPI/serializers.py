from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Fields:
    - id: Unique identifier
    - slug: Category slug
    - title: Category name
    """
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the MenuItem model.
    Fields:
    - id: Unique identifier
    - title: Menu item name
    - price: Menu item price
    - featured: Boolean indicating if the item is featured
    - category: Category data (read-only)
    - category_id: Category ID (write-only)

    Validations:
    - The combination of title and price must be unique.
    """
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
    """
    Serializer for the User model.
    Fields:
    - id: Unique identifier
    - username: Username
    - email: User email
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    Fields:
    - user: Owner of the cart (read-only)
    - menuitem: Menu item added to the cart
    - unit_price: Price per unit of the item (read-only)
    - quantity: Quantity of the item in the cart
    - price: Total price for this item (read-only)

    Methods:
    - create(): Automatically assigns the authenticated user when creating a Cart.
    """
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default = serializers.CurrentUserDefault()
    )
    unit_price = serializers.DecimalField(
        source='menuitem.price',
        max_digits=6,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        read_only_fields=['user', 'unit_price', 'price']
        
    def create(self, validated_data):
        user = self.context['request'].user
        return Cart.objects.create(user=user, **validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    Fields:
    - order: Order this item belongs to
    - menuitem: Menu item
    - quantity: Quantity of the item
    - price: Total price for this item in the order
    """
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']
    

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    Fields:
    - id: Unique identifier of the order
    - user: User who placed the order
    - delivery_crew: User assigned for delivery
    - status: Order status
    - date: Order creation date
    - total: Total order price
    - orderitem: List of order items (read-only)
    """
    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'date', 'total', 'orderitem']