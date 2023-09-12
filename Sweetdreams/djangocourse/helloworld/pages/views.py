from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError 
from .models import Product, Category, Organization
from random import sample

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén tres productos aleatorios de la base de datos
        random_products = sample(list(Product.objects.all()), 3)
        context['title'] = 'Home Page - SweetDreams'
        context['random_products'] = random_products  # Pasa los productos aleatorios al contexto
        return context
    
class ProductFilterForm(forms.Form):
    # Agrega los campos que desees para filtrar, por ejemplo, una categoría
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Todas las Categorías",
        required=False
    )
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        empty_label="Todas las Compañías",
        required=False
    )

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        
        # Obtén el formulario de filtrado y procesa los datos enviados por el usuario
        filter_form = ProductFilterForm(request.GET)
        if filter_form.is_valid():
            category = filter_form.cleaned_data.get('category')
            organization = filter_form.cleaned_data.get('organization')
            # Filtra los productos en función de los parámetros del formulario
            products = Product.objects.all()
            if category:
                products = products.filter(category=category)
            if organization:
                products = products.filter(organization=organization)
        # Agrega los productos filtrados y el formulario al contexto
        viewData["products"] = products
        viewData["filter_form"] = filter_form
        
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        try:
            product_id=int(id)
            if 1<= int(id):
                viewData = {}
                product = get_object_or_404(Product, pk=product_id)
                viewData["title"] = product.name + " - Online Store"
                viewData["subtitle"] = product.name + " - Product information"
                viewData["product"] = product
                return render(request, self.template_name, viewData)
            else:
                return HttpResponseRedirect(reverse('home'))
        except ValueError:
            return HttpResponseRedirect(reverse('home'))
    def post(self, request, id):
        product_id = request.POST.get('product_id')  # Obtén el ID del producto del formulario
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return redirect('home')
        except Product.DoesNotExist:
            pass  # Manejar el caso en que el producto no existe
        return redirect('home')
        

class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        products = Product.objects.all()
        cart_product_data = request.session.get('cart_product_data', {})
        cart_products = [product for product in products if str(product.id) in cart_product_data.keys()]
        cart_total = sum([product.price for product in cart_products])
        view_data = {
            'title': 'SweetDreams - Cart',
            'subtitle': 'Shopping Cart',
            'cart_products': cart_products,
            'cart_total': cart_total
        }
        return render(request, self.template_name, view_data)

class AddToCartView(View):
    def post(self, request, product_id):
        product_id = request.POST.get('product_id')
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data
        return redirect('index')

class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']
        return redirect('cart')
