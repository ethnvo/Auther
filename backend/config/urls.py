from django.contrib import admin
from django.urls import path, include
#from api.views import home  # optional welcome view

urlpatterns = [
  #  path('', home),  # homepage JSON response
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # includes app-level routes
]
