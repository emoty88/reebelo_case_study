from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_CHOICES = (
        ("processing", "Processing"),
        ("cancelled", "Cancelled"),
        ("delivered", "Delivered"),
    )
    total = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="processing")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='order_products')
    quantity = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(pre_save, sender=OrderProduct)
def order_product_pre_save(sender, instance, **kwargs):
    instance.total = instance.product.price * instance.quantity 


@receiver(post_save, sender=OrderProduct)
def order_product_post_save(sender, instance, created, **kwargs):
    order = instance.order
    order.total = order.order_products.aggregate(models.Sum('total'))['total__sum']
    order.save()
    