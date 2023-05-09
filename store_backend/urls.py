from django.contrib import admin
from django.urls import path, include

from api.router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Api URLs
    path('api/v1/', include(router.urls)),
]
