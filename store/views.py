import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Category

# Create your views here.

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
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

def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)

    if cart_item.user == request.user or cart_item.user is None:
        cart_item.delete()

    return redirect('view_cart') 

stripe.api_key = settings.STRIPE_SECRET_KEY  

def checkout(request):
    if request.method == "POST":
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item.product.name},
                        "unit_amount": int(item.product.price * 100),
                    },
                    "quantity": item.quantity,
                }
                for item in cart_items
            ],
            mode="payment",
            success_url="http://127.0.0.1:8000/success/",
            cancel_url="http://127.0.0.1:8000/cart/",
        )

        return redirect(session.url)

    return render(request, "store/checkout.html")

def payment_success(request):
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()


    return render(request, "store/success.html")


def update_cart(request, pk, action):
    cart_item = get_object_or_404(Cart, pk=pk)

    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # If quantity reaches 0, remove from cart

    return redirect('view_cart')

def category_page(request, category_name):
    products = Product.objects.filter(category__name=category_name)
    return render(request, 'store/product_list.html', {'products': products})


