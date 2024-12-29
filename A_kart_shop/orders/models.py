from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')  # Through table for quantity and price
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Cancelled', 'Cancelled'),
            ('Completed', 'Completed')
        ],
        default='Pending'
    )
    seller_approval = models.BooleanField(null=True, blank=True)  # None = Pending, True = Approved, False = Cancelled

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity * self.product.get_final_price()

    def __str__(self):
        return f"Cart: {self.user.username} - {self.product.name} ({self.quantity})"

