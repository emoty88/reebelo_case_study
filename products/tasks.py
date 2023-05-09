from celery import shared_task
from products.models import Product, Order, OrderProduct
from django.db.models import Sum, Count
from datetime import date, timedelta
from products.utils import time_consuming_task

@shared_task
def order_placed(order_id=None):
    # order = Order.objects.get(id=order_id)
    send_order_confirmation_notification.apply_async(args=[order_id])
    update_quantity.apply_async(args=[order_id])
    

@shared_task
def send_order_confirmation_notification(order_id=None):
    order = Order.objects.get(id=order_id)
    #Demonstrate doing some time consuming task after order is placed
    time_consuming_task()
    print(f"Order confirmation notification sent for order id: {order.id}")


@shared_task
def update_quantity(order_id=None):
    order = Order.objects.get(id=order_id)
    order_products = OrderProduct.objects.filter(order_id=order.id)
    for order_product in order_products:
        product = Product.objects.get(id=order_product.product_id)
        product.quantity -= order_product.quantity
        product.save()
    print(f"Product quantity updated for order id: {order.id}")