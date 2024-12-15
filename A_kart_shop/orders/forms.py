from django import forms
from store.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'sale_price', 'description', 'category', 'sub_category', 'is_on_sale']
