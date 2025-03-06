from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    else:
        cart_item, created = Cart.objects.get_or_create(user=None, product=product)

    if not created:
        cart_item.quantity += 1  # Increase quantity if already in cart
        cart_item.save()

    return redirect('view_cart')

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = Cart.objects.filter(user=None)  # Guest users (optional)

    return render(request, 'store/cart.html', {'cart_items': cart_items})
