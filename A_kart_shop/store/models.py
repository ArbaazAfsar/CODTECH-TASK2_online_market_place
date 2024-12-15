from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # Seller is a user
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='upload/product', null=False)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=20, null=True, blank=True)  # Optional discount price
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    is_on_sale = models.BooleanField(default=False)  # Flag to indicate if product is on sale

    def __str__(self):
        return self.name

    def get_final_price(self):
        """Return sale price if on sale, else regular price."""
        return self.sale_price if self.is_on_sale else self.price
    
    
    
 

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you are associating reviews with products or courses
    rating = models.PositiveIntegerField()  # Rating out of 5
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"