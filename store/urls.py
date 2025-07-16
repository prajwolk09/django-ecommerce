from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('products/<slug:slug>',views.product_detail,name='product_detail'),

    path('cart/',views.cart,name='cart'),
    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
]
