from django.db import models

from django.db import models

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
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='upload/product', null=False)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

