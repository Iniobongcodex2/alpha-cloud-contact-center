from django.contrib import admin
from django.urls import path, include

# Customize the Django Admin to match ALPHA branding
admin.site.site_header = "ALPHA Cloud Contact Center"
admin.site.site_title = "ALPHA Admin Portal"
admin.site.index_title = "Welcome to the ALPHA Operations Center"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]