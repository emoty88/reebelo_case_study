from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.cache import cache

# from django_auto_prefetching import AutoPrefetchViewSetMixin
from api.serializers import *
from products.models import *


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        order_products = request.data.pop('order_products')
        order_serializer = self.get_serializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.validated_data['user_id'] = request.user.id
        order_serializer.validated_data['total'] = 0
        order = order_serializer.save()
        for order_product in order_products:
            print(order_product)
            order_product['order'] = order.id
            order_product_serializer = OrderProductSerializer(data=order_product)
            order_product_serializer.is_valid(raise_exception=True)
            print(order_product_serializer.validated_data)
            order_product_serializer.save()

        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    

@method_decorator(csrf_exempt, name='dispatch')
class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        cart_items = cache.get(f'cart-{request.user.id}', [])
        return Response(cart_items)
    
    def create(self, request):
        cart_items = cache.get(f'cart-{request.user.id}', [])
        serialize = CartSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)

        #check if product is already in cart then update quantity
        item_exists = False
        for cart_item in cart_items:
            if cart_item['product_id'] == serialize.validated_data['product_id']:
                cart_item['quantity'] += serialize.validated_data['quantity']
                item_exists = True

        if not item_exists:
            cart_items.append(serialize.validated_data)
        
        cache.set(f'cart-{request.user.id}', cart_items)
        return Response(cart_items, status=status.HTTP_201_CREATED)

