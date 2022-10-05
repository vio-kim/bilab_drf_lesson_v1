from django.contrib import admin
from django.urls import path, include


api_patterns = [
    path('products/', include('products.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_patterns))
]
