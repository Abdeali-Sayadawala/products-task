from django import forms
from .models import Product, Category


class ProductFrom(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'product_code', 'price', 'category', 'manufacture_date', 'expiry_date', 'status')

class CategoryFrom(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'sub_category')