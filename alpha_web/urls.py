from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Customize Admin branding
admin.site.site_header = "ALPHA Cloud Contact Center"
admin.site.site_title = "ALPHA Admin Portal"
admin.site.index_title = "Welcome to ALPHA Operations"

urlpatterns = [
    path('admin/', admin.site.urls),
    # Built-in Login and Logout Views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Your App URLs
    path('', include('core.urls')),
]