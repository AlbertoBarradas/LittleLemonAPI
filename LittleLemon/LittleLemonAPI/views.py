import json
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Category, MenuItem, Order, OrderItem, Cart
from rest_framework import generics, status, viewsets, filters, permissions
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, UserSerializer, OrderSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from .permissions import IsInManagerGroup, IsManagerOrSuperAdmin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination

class MenuItemsListCreate(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'category__title']
    ordering_fields = ['title', 'price']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 4
    pagination_class.page_query_param = 'pagenum'
    pagination_class.page_size_query_param = 'page'
    pagination_class.max_page_size = 20
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [permissions.AllowAny()]

class MenuItemsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        if self.request.method == 'DELETE' or self.request.method == 'PUT' or self.request.method == 'PATCH':
            return [IsInManagerGroup()]
        return [permissions.AllowAny()]

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class CartListCreate(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.filter(user=self.request.user)
        return cart
    
    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("ok")

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count()==0:
            return Order.objects.filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.all()
        
    def create(self, request, *args, **kwargs):
        menuitem_count = Cart.objects.filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message": "no item in cart"})
        
        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        if(order_serializer.is_valid()):
            order = order_serializer.save()

            items = Cart.objects.filter(user=self.request.user)

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    menuitem=item.menuitem,
                    price=item.price,
                    quantity=item.quantity,
                    unit_price=item.menuitem.price
                )
            
            
            items.delete()

            result = order_serializer.data.copy()
            result['total'] = total
            return Response(result, status=201)
        
        return Response(order_serializer.errors, status=400)


    def get_total_price(self, user):
        total = 0
        items = Cart.objects.filter(user=user)
        for item in items:
            total += item.price
        return total
    
class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0:
            return Response('Not OK')
        else:
            return super().update(request, *args, **kwargs)
    

@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    manager = Group.objects.get(name="Manager")
    if request.method == 'GET':
            users = manager.user_set.all().values('id','username','email')
            return Response(users)
    
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        manager = Group.objects.get(name="Manager")
        if request.method == 'POST':
            manager.user_set.add(user)
            return Response({"message":"user added to manager group"})
        elif request.method == 'DELETE':
            manager.user_set.remove(user)
            return Response({"message":"user removed from manager group"})
        
        
    return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    delivery_crew = Group.objects.get(name="Delivery crew")
    if request.method == 'GET':
        users = delivery_crew.user_set.all().values('id', 'username', 'email')
        return Response(users)
    
    if not IsManagerOrSuperAdmin().has_permission(request, delivery_crew):
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        if request.method == 'POST':
            delivery_crew.user_set.add(user)
            return Response({"message":"user added to delivery crew group"})
        elif request.method == 'DELETE':
            delivery_crew.user_set.remove(user)
            return Response({"message":"user removed from delivery crew group"})
        
    return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)
    
