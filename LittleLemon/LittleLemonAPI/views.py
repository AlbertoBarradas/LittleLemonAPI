import json
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Category, MenuItem, Order, OrderItem, Cart
from rest_framework import generics, status, viewsets, filters, permissions
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, UserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from .permissions import IsInManagerGroup

# Create your views here.
class MenuItemsListCreate(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'category']
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInManagerGroup()]
        return [permissions.AllowAny()]

class MenuItemsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        if self.request.method == 'DELETE' or self.request.method == 'PUT' or self.request.method == 'PATCH':
            return [IsInManagerGroup()]
        return [permissions.AllowAny()]

class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsInManagerGroup]

class CartListCreate(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartDestroy(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsInManagerGroup])
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
@permission_classes([IsInManagerGroup])
def delivery_crew(request):
    delivery_crew = Group.objects.get(name="Delivery crew")
    if request.method == 'GET':
        users = delivery_crew.user_set.all().values('id', 'username', 'email')
        return Response(users)
    
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
    
