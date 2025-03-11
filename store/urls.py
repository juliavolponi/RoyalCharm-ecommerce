from django.urls import path
from .views import product_list, product_detail, add_to_cart, view_cart, remove_from_cart

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
]
