from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Category, MenuItem, Order, OrderItem, Cart
from rest_framework import generics, status, viewsets, filters
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Create your views here.
class MenuItemsListCreate(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'category']

class CategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsRetrieve(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        manager = Group.objects.get(name="Manager")
        if request.method == 'POST':
            manager.user_set.add(user)
        elif request.method == 'DELETE':
            manager.user_set.remove(user)
        return Response({"message":"user added to manager group"})
    return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)