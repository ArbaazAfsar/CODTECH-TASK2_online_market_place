from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, SubCategory,Review
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm

def home(request):
    # Order products by 'id' or another appropriate field to ensure consistent pagination
    prodects = Product.objects.all().order_by('id')  # Replace 'id' with the desired field for ordering
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
            'prodects': category_products,
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

        return render(request, 'subCategory.html', {
            'categories': categories,
            'category_products': products,
            'sub_categories': sub_categories,
            'selected_sub_category': sub_category,
        })
    except SubCategory.DoesNotExist:
        messages.error(request, 'This sub-category does not exist.')
        return redirect('home')

def products(request, pk):
    product = get_object_or_404(Product, id=pk)  # Fetch single product
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    reviews = Review.objects.filter(product=product)  # Fetch reviews for the product
    
    return render(request, "product.html", {
        'product': product,  # Single product variable, not plural
        'categories': categories,
        'sub_categories': sub_categories,
        'reviews': reviews,
    })
    
    
@login_required(login_url='login')
@login_required
def add_review(request, product_id):
    product = Product.objects.get(id=product_id)  # Fetch product based on the ID
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product', pk=product.id)  # Redirect to product detail page with pk
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'product': product})

from fuzzywuzzy import fuzz

from django.db.models import Q

from django.db.models import Q

from django.db.models import Q

def search_results(request):
    search_query = request.GET.get('search', '')
    
    # If there is no search query, return all products
    if not search_query:
        products = Product.objects.all()
        Categorys = Category.objects.all()
        Subcategorys = SubCategory.objects.all()
    else:
        # Construct Q objects for matching on name, category, and subcategory
        name_condition = Q(name__icontains=search_query)
        category_condition = Q(category__name__icontains=search_query)
        subcategory_condition = Q(sub_category__name__icontains=search_query)

        # Combine all conditions with OR and filter products
        products = Product.objects.filter(
            name_condition | category_condition | subcategory_condition
        )

        # Fetch categories and subcategories for the template
        Categorys = Category.objects.filter(name__icontains=search_query)  # Fix here
        Subcategorys = SubCategory.objects.filter(name__icontains=search_query)

    return render(request, 'search_results.html', {
        'search_query': search_query,
        'products': products,
        'Categorys': Categorys,
        'Subcategorys': Subcategorys
    })


def advanced_search(request):
    categories = Category.objects.all()
    return render(request, 'advanced_search.html', {'categories': categories})