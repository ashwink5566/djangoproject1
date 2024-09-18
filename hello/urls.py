
from django.contrib import admin
from django.urls import path, include  # Correct import statement

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),  # Include the URLs from the 'base' app
    path('api/', include('base.api.urls')),
]


