from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
def home(request):
    return render(request,'store/home.html')

def products(request):
    products = Product.objects.filter(is_active=True)
    return render(request,'store/products.html', {'products':products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/product_detail.html', {'product':product})

@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, item in cart.items():
        item_subtotal = float(item['price']) * item['quantity']
        total += item_subtotal
        cart_items.append({
            'product_id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': "%.2f" % item_subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total': "%.2f" % total,
    }

    return render(request,'store/cart.html',context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = request.session.get('cart',{})

    #GEt quantity from cart, default to 1
    quantity = int(request.POST.get('quantity',1))

    #If the product is already in the cart
    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] +=1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': quantity
        }

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('products')

def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart',{})
        quantity = int(request.POST.get('quantity',1))

        if str(product_id) in cart:
            if quantity > 0:
                cart[str(product_id)]['quantity'] = quantity
            else:
                cart.pop(str(product_id))

            request.session['cart'] = cart
            request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart',{})

    if str(product_id) in cart:
        cart.pop(str(product_id))
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,'store/dashboard.html')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            qty = quantity['quantity'] if isinstance(quantity, dict) else quantity
            subtotal = product.price * qty
            cart_items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })
            total += subtotal
        except Product.DoesNotExist:
            continue

    if request.method == 'POST':
        if not cart_items:
            messages.warning(request, "Your cart is empty!")
            return redirect('cart')

        order = Order.objects.create(user=request.user, total=total)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price  # snapshot price
            )
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")
        return redirect('dashboard')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })