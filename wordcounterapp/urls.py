from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # Links the main 'counter' app URLs to the root (homepage) of the site
    path("", include('counter.urls')),
]
