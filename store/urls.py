from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('products/<slug:slug>',views.product_detail,name='product_detail'),

    path('cart/',views.cart_detail,name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),


    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
]
