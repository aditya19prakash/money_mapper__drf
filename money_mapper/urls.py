
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transaction/',include('transaction.urls')),
    path('user/',include('user.urls')),
    path('category/',include('category.urls'))
]
