import os
from celery import shared_task
from products.models import Product, Order, OrderProduct
from django.db.models import Sum, Count
from datetime import date, timedelta
from products.utils import time_consuming_task
from elasticsearch import Elasticsearch

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


@shared_task
def synch_product_to_elastic(product_id=None, created=False):
    product = Product.objects.get(id=product_id)

    ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD', 'qwer1234')
    es = Elasticsearch(f'http://elastic:{ELASTIC_PASSWORD}@es01:9200', verify_certs=False)
    # Define the index and document ID
    index_name = 'products'
    doc_id = product_id

    if es.exists(index_name, id=doc_id):
        doc = es.get(index=index_name, id=doc_id)['_source']
        doc['quantity'] = product.quantity
        doc['price'] = product.price
        doc['name'] = product.name
        doc['description'] = product.description
        doc['image'] = product.image.url
        doc['created_at'] = product.created_at
        doc['updated_at'] = product.updated_at

        es.update(index=index_name, id=doc_id, body={'doc': doc})
    else:
        doc = {
            'quantity': product.quantity,
            'price': product.price,
            'name': product.name,
            'description': product.description,
            'image': product.image.url if product.image else '',
            'created_at': product.created_at,
            'updated_at': product.updated_at,
        }
        es.create(index=index_name, id=doc_id, body=doc)

    print(f"Product synced to elastic search for product id: {product_id}")