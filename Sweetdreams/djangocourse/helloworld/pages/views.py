from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Product, Category, Organization, ProductJson
from random import sample
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import json
from django.conf import settings
from .forms import JSONUploadForm
import googlemaps
import datetime 
from django.http import FileResponse
from django.template import Context
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from django.contrib.auth.decorators import login_required
import os
# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén tres productos aleatorios de la base de datos
        random_products = sample(list(Product.objects.all()), 3)
        context["title"] = "Home Page - SweetDreams"
        context[
            "random_products"
        ] = random_products  # Pasa los productos aleatorios al contexto
        return context


class ProductFilterForm(forms.Form):
    # Agrega los campos que desees para filtrar, por ejemplo, una categoría
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Todas las Categorías",
        required=False,
    )
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        empty_label="Todas las Compañías",
        required=False,
    )


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"

        # Obtén el formulario de filtrado y procesa los datos enviados por el usuario
        filter_form = ProductFilterForm(request.GET)
        if filter_form.is_valid():
            category = filter_form.cleaned_data.get("category")
            organization = filter_form.cleaned_data.get("organization")
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
    template_name = "products/show.html"

    def get(self, request, id):
        try:
            product_id = int(id)
            if 1 <= int(id):
                viewData = {}
                product = get_object_or_404(Product, pk=product_id)
                viewData["title"] = product.name + " - Online Store"
                viewData["subtitle"] = product.name + " - Product information"
                viewData["product"] = product
                return render(request, self.template_name, viewData)
            else:
                return HttpResponseRedirect(reverse("home"))
        except ValueError:
            return HttpResponseRedirect(reverse("home"))

    def post(self, request, id):
        product_id = request.POST.get(
            "product_id"
        )  # Obtén el ID del producto del formulario
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return redirect("home")
        except Product.DoesNotExist:
            pass  # Manejar el caso en que el producto no existe
        return redirect("home")


class CartView(View):
    template_name = "cart/index.html"

    def get(self, request):
        products = Product.objects.all()
        cart_product_data = request.session.get("cart_product_data", {})
        cart_products = [
            product
            for product in products
            if str(product.id) in cart_product_data.keys()
        ]

        # Actualizar cart_products para incluir la cantidad
        for product in cart_products:
            product.quantity = cart_product_data[str(product.id)]

        cart_total = sum(
            [product.price * product.quantity for product in cart_products]
        )
        view_data = {
            "title": "SweetDreams - Cart",
            "subtitle": "Shopping Cart",
            "cart_products": cart_products,
            "cart_total": cart_total,
        }
        return render(request, self.template_name, view_data)


class AddToCartView(View):
    def post(self, request, product_id):
        product_id = request.POST.get("product_id")
        cart_product_data = request.session.get("cart_product_data", {})
        cart_product_data[product_id] = int(cart_product_data.get(product_id, 0)) + int(request.POST.get('quantity'))
        request.session["cart_product_data"] = cart_product_data
        return redirect("index")


class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if "cart_product_data" in request.session:
            del request.session["cart_product_data"]
        return redirect("cart")


def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
        view_data = {"form": form}
        return render(request, "sign/signup.html", view_data)
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                # Redirige al usuario a la página de registro con un parámetro "success"
                return HttpResponseRedirect(f"{reverse('signup')}?success=1")
            except Exception as e:
                return HttpResponseRedirect(f"{reverse('signup')}?user=1")
        return HttpResponseRedirect(f"{reverse('signup')}?password=1")


def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        form = AuthenticationForm()
        view_data = {"form": form}
        return render(request, "sign/signin.html", view_data)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            view_data = {"form": form}
            return render(request, "sign/signin.html", view_data)


class ProductSearch(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = 'products'  # El nombre que se usará en la plantilla para los objetos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = ProductFilterForm(self.request.GET)
        context["title"] = "Products - Online Store"
        context["subtitle"] = "List of products"
        context['filter_form'] = filter_form
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(name__icontains=query).order_by('name')

def export_products_to_json(request):
    products = Product.objects.all()
    products_data = [{'name': product.name, 
                    'price': product.price,
                    'created_at': str(product.created_at),
                    'updated_at': str(product.updated_at),
                    'category': str(product.category),
                    'organization': str(product.organization),
                    'image_url': "http://35.223.74.49:8000"+settings.MEDIA_URL + str(product.image)} for product in products]
    json_data = json.dumps(products_data, indent=2)
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="products.json"'
    return response

def display_json(request):
    products = ProductJson.objects.all()
    return render(request, 'json/display_json.html', {'products': products})
    
def upload_json(request):
    if request.method == 'POST':
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['json_file']
            ProductJson.objects.all().delete()
            try:
                data = json.load(uploaded_file)
                for item in data:
                    ProductJson.objects.create(
                        description=item['description'],
                        productJson_id=item['id'],
                        name=item['name'],
                        price=item['price'],
                        product_image=item['product_image']
                    )
                return redirect('display_json')
            except json.JSONDecodeError:
                # Manejar errores si el JSON no es válido
                pass
        else:
            form.add_error(None, 'Please select a JSON file to upload.')
    else:
        form = JSONUploadForm()

    return render(request, 'json/upload_json.html', {'form': form})

class GeneratePDFView(View):
    def get(self, request):
        user = request.user
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, letter[1] - 50, "Shopping Cart")       
        # Obtener datos del carrito
        cart_product_data = request.session.get("cart_product_data", {})
        y = letter[1] - 100
        for product_id, quantity in cart_product_data.items():
            try:
                product = Product.objects.get(pk=product_id)
                product_name = product.name
                product_price = product.price
                p.drawString(100, y, f"Name: {product_name} - Price: ${product_price} - Quantity: {quantity}")
                y -= 20
            except Product.DoesNotExist:
                pass
        cart_total = sum(
            [product.price * cart_product_data[product_id] for product_id in cart_product_data]
        )
        p.drawString(100, y, f"Total Cart Price: ${cart_total}")
        p.drawString(300, y, f"User: {user.username}")
        p.drawString(300, y - 20, f"Email: {user.email}")
        p.showPage()
        p.save()
        buffer.seek(0)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cart.pdf"'
        response.write(buffer.read())

        if "cart_product_data" in request.session:
            del request.session["cart_product_data"]
        return response