from rest_framework import viewsets, status
from rest_framework.response import Response
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

