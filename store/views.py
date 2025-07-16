from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product
from django.shortcuts import get_object_or_404

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
def cart(request):
    return render(request,'store/cart.html')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = request.session.get('cart',{})

    #If the product is already in the cart
    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] +=1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1
        }

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