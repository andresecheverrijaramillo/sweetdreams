from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError 
from .models import Product

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    

class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
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
        
class ProductListView(ListView): 
    model = Product 
    template_name = 'product_list.html' 
    context_object_name = 'products'  # This will allow you to loop through 'products' in your template 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Products - Online Store' 
        context['subtitle'] = 'List of products' 
        return context    
        
class ProductForm(forms.ModelForm):
        class Meta: 
            model = Product 
            fields = ['name', 'price'] 

        def clean_price(self): 
            price = self.cleaned_data.get('price') 
            if price is not None and price <= 0: 
                raise ValidationError('Price must be greater than zero.') 
            return price 

class ProductCreateView(View):
    template_name = 'products/create.html'
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid(): 
            form.save() 
            return redirect('created')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        
class ProductCreatedView(View):
    template_name = 'products/created.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Product Created"
        return render(request, self.template_name, viewData)