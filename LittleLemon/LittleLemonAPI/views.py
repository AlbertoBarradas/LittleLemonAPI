from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Category, MenuItem, Order, OrderItem, Cart
from rest_framework import generics, status, viewsets
from django.contrib.auth.models import User
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.permissions import IsAdminUser

# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class CategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer