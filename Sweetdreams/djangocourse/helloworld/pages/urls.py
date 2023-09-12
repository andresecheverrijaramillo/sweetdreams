from django.urls import path
from .views import HomePageView, ProductIndexView, ProductShowView, CartView, AddToCartView, CartRemoveAllView
urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path('products/', ProductIndexView.as_view(), name='index'),
    path('products/<str:id>', ProductShowView.as_view(), name='show'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<str:product_id>', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
]