from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.products, name='product'),
    path('category/<str:name>/', views.categorys, name='category'),
    path('subcategory/<str:name>/', views.subCategory, name='subcategory'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('search/', views.search_results, name='search_results'),
    path('advanced_search/', views.advanced_search, name='advanced_search'),

    
]