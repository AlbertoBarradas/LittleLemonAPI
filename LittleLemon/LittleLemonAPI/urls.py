from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', views.MenuItemsListCreate.as_view()),
    path('menu-items/<int:pk>/', views.MenuItemsRetrieveUpdateDestroy.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('category/', views.CategoryCreate.as_view()),
    path('groups/manager/users/', views.managers),
    path('groups/delivery-crew/users/', views.delivery_crew),
    path('api-token-auth/', obtain_auth_token),
    path('cart/menu-items/', views.CartListCreate.as_view()),
    path('orders/', views.OrderView.as_view()),
    path('orders/<int:pk>/', views.SingleOrderView().as_view()),
]