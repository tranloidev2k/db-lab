from django.db import models
from django.db.models import Q
from django.db.models.functions import Upper

class UsersDemo(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.TextField()
    country = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users_demo'

class Customer(models.Model):
    email = models.CharField(max_length=255)
    country = models.CharField(max_length=2)
    created_at = models.DateTimeField()
    is_verified = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["country", "created_at"],
                include=["email"],
                name="customer_country_created_idx",
            ),
            models.Index(
                fields=["created_at"],
                condition=Q(is_verified=False),
                name="customer_unverified_idx",
            ),
            models.Index(
                Upper("email"),
                name="customer_email_upper_idx",
            ),
        ]

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField()
    status = models.CharField(max_length=20)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()