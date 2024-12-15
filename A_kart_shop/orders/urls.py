from django.urls import path
from . import views

urlpatterns = [
    path('list-product/', views.list_product, name='list_product'),
    path('seller/products/', views.seller_products, name='seller_products'),
    path('buy-product/<int:product_id>/', views.buy_product, name='buy_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    
]
