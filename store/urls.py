from django.contrib.auth import views as auth_views
from django.urls import path
from .views import product_list, product_detail, add_to_cart, view_cart, remove_from_cart, checkout, payment_success, update_cart, category_page, register

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path("checkout/", checkout, name="checkout"),
    path("success/", payment_success, name="payment_success"),
    path('update-cart/<int:pk>/<str:action>/', update_cart, name='update_cart'),
    path('category/<str:category_name>/', category_page, name='category_page'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', register, name='register'),
]
