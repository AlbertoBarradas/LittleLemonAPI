from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', views.MenuItemsListCreate.as_view()),
    path('menu-items/<int:pk>/', views.MenuItemsRetrieve.as_view()),
    path('category/', views.CategoryCreate.as_view()),
    path('groups/manager/users/', views.managers),
    path('api-token-auth/', obtain_auth_token),
]