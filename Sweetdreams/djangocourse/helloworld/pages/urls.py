from django.urls import path
from .views import (
    HomePageView,
    ProductIndexView,
    ProductShowView,
    CartView,
    AddToCartView,
    CartRemoveAllView,
    signup,
    signout,
    signin,
    ProductSearch,
    export_products_to_json,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("products/", ProductIndexView.as_view(), name="index"),
    path("products/<str:id>", ProductShowView.as_view(), name="show"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/<str:product_id>", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/removeAll", CartRemoveAllView.as_view(), name="cart_removeAll"),
    path("signup/", signup, name="signup"),
    path("signout/", signout, name="signout"),
    path("signin/", signin, name="signin"),
    path('search_products/', ProductSearch.as_view(), name='search_products'),
    path('export-products-json/', export_products_to_json, name='export_products_json'),
]
