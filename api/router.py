from rest_framework.routers import DefaultRouter
from api.views import *


router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'orders', OrderViewSet, basename='orders')