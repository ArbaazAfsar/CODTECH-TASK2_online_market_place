from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.products, name='product'),
    path('category/<str:name>/', views.categorys, name='category'),
    path('subcategory/<str:name>/', views.subCategory, name='subcategory'),
    path('subcategory/<str:name>/', views.subCategory, name='subcategory'),
    
    
]