from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls', namespace='name')),
    path('admin/', admin.site.urls),
]
