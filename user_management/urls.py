from django.contrib import admin
from django.urls import path, include 
import x

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('x.urls')),
]