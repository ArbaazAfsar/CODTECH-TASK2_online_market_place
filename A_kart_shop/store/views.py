from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, SubCategory,Review
from orders.models import Cart
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from orders.forms import ProductForm

from django.db.models import Q

def home(request):
    products = Product.objects.all().order_by('id')  # Order as needed
    paginator = Paginator(products, 8)  # 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    Categories = Category.objects.all()
    sub_category_products = SubCategory.objects.all()
    
    # Precompute filled and empty stars for each product
    for product in products:
        avg_rating = product.get_average_rating()  # This will give the rounded rating
        product.filled_stars = avg_rating  # Use the rounded average for filled stars
        product.empty_stars = 5 - avg_rating  # Use the remaining stars for empty stars
    
    return render(request, 'home.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'Categories': Categories,
        'sub_category_products': sub_category_products
    })



def categorys(request, name):
    categories = Category.objects.all()
    try:
        category = Category.objects.get(name=name)
        category_products = Product.objects.filter(category=category)
        
        # Pagination
        paginator = Paginator(category_products, 8)  
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        
        sub_categories = SubCategory.objects.filter(parent=category)
        
        return render(request, 'category.html', {
            'categories': categories,
            'products': page_obj,
            'sub_categories': sub_categories,
            'selected_category': category,
            'page_obj': page_obj,
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
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    # Update the cart with the new quantity if POST request is made
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('products', pk=product.id)  # Redirect to the same product page after adding to cart
    
    return render(request, "product.html", {
        'product': product,
        'categories': categories,
        'sub_categories': sub_categories,
        'reviews': reviews,
        'cart_item': cart_item,
    })
    
    
@login_required(login_url='login')
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    existing_review = Review.objects.filter(user=request.user, product=product).first()
    
    if existing_review:
        messages.info(request, 'You have already reviewed this product.')
        return redirect('product', pk=product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('product', pk=product.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'product': product})



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


