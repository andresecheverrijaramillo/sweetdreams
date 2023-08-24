from django.urls import path
from .views import HomePageView, ProductIndexView, ProductShowView, ProductCreateView, ProductCreatedView
urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path('products/', ProductIndexView.as_view(), name='index'),
    path('products/create', ProductCreateView.as_view(), name='form'),
    path('products/created', ProductCreatedView.as_view(), name='created'),
    path('products/<str:id>', ProductShowView.as_view(), name='show'),
]