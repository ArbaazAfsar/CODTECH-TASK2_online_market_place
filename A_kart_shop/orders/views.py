from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import  Order, Cart, OrderItem
from store.models import Product
from django.db.models import Sum, F
from django.db import transaction  
from decimal import Decimal


@login_required
def list_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Set the seller to the current user
            product.save()
            return redirect('home')  # Redirect to a list of products or success page
    else:
        form = ProductForm()

    return render(request, 'list_product.html', {'form': form})

@login_required
def seller_products(request):
    # Filter products by the logged-in seller
    products = Product.objects.filter(seller=request.user)
    return render(request, 'seller_products.html', {'products': products})



@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Create the Order instance first
        order = Order.objects.create(
            user=request.user,
            total_price=product.get_final_price(),  # Initial price, will be updated later
        )

        # Create the OrderItem instance related to the created Order
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,  # You can change this if you collect quantity from the form
            total_price=product.get_final_price()
        )

        # Update the total_price of the order after creating the OrderItem
        order.total_price = order_item.total_price  # Add logic if multiple items
        order.save()

        # Redirect to the success page with the order ID
        return redirect('order_success', order_id=order.id)

    return render(request, 'buy_product.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:  # If product already exists in the cart, just increment the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')  # Redirect to the cart page after adding the product



@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    # Define tax rate (e.g., 18%) as a Decimal
    tax_rate = Decimal('0.18')
    tax_amount = subtotal * tax_rate
    total_amount = subtotal + tax_amount

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax_rate': tax_rate * 100,  # Display as a percentage
        'tax_amount': tax_amount,
        'total_amount': total_amount,
    }
    return render(request, 'view_cart.html', context)


@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()

    return redirect('view_cart')



@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')



@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('view_cart')  # Redirect to the cart if empty

    with transaction.atomic():  # Ensure atomic transaction
        # Create the Order instance
        order = Order.objects.create(user=request.user)

        # Create related OrderItem instances and calculate the total price
        total_price = 0
        for cart_item in cart_items:
            item_total_price = cart_item.quantity * cart_item.product.get_final_price()
            total_price += item_total_price
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                total_price=item_total_price,
            )

        # Update the total price of the order
        order.total_price = total_price
        order.save()

        # Clear the cart after order is placed
        cart_items.delete()

    return redirect('order_success', order_id=order.id)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})
