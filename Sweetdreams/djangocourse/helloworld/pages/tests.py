from django.test import TestCase
from .models import Product, Category, Organization

# Create your tests here.

class unitTest(TestCase):
    def test_product_fields(self):
        product = Product()
        product.name = "Test Product"
        product.price = 100
        product.description = "Test Product Description"
        product.category = Category.objects.create(name="Test Category")
        product.organization = Organization.objects.create(name="Test Organization")
        product.save()

        record = Product.objects.get(pk=1)
        self.assertEqual(record, product)

    def test_category_fields(self):
        category = Category()
        category.name = "Test Category"
        category.save()

        record = Category.objects.get(pk=1)
        self.assertEqual(record, category)

    def test_organization_fields(self):
        organization = Organization()
        organization.name = "Test Organization"
        organization.save()

        record = Organization.objects.get(pk=1)
        self.assertEqual(record, organization)