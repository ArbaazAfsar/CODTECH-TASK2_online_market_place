from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, SubCategory
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    prodects = Product.objects.all()
    paginator = Paginator(prodects, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    Categories = Category.objects.all()
    sub_category_products = SubCategory.objects.all()
    return render(request, 'home.html', {
        'prodects': page_obj,
        'page_obj': page_obj,
        'Categories': Categories,
        'sub_category_products': sub_category_products
    })

def categorys(request, name):
    categories = Category.objects.all()
    try:
        category = Category.objects.get(name=name)
        category_products = Product.objects.filter(category=category)
        sub_categories = SubCategory.objects.filter(parent=category)
        
        return render(request, 'category.html', {
            'categories': categories,
            'category_products': category_products,
            'sub_categories': sub_categories,
            'selected_category': category,
        })
    except Category.DoesNotExist:
        messages.error(request, 'This category does not exist.')
        return redirect('home')

def subCategory(request, name):
    categories = Category.objects.all()
    try:
        sub_category = SubCategory.objects.get(name=name)
        products = Product.objects.filter(sub_category=sub_category)
        sub_categories = SubCategory.objects.filter(parent=sub_category.parent)  # Fetch siblings

        return render(request, 'category.html', {
            'categories': categories,
            'category_products': products,
            'sub_categories': sub_categories,
            'selected_sub_category': sub_category,
        })
    except SubCategory.DoesNotExist:
        messages.error(request, 'This sub-category does not exist.')
        return redirect('home')

def products(request, pk):
    product = get_object_or_404(Product, id=pk)
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    return render(request, "product.html", {
        'product': product,
        'categories': categories,
        'sub_categories': sub_categories,
    })
