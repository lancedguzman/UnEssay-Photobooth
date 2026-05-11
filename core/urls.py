"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from photobooth import views as booth_views
from photo_capture import views as photo_views
from gif_capture import views as gif_views

urlpatterns = [
        # Admin Route
    path('admin/', admin.site.urls),

    # Include app-specific URLs
    path('', include('photobooth.urls')),

    # Orchestrator Routes
    path('', booth_views.landing, name='home'),
    path('result/<uuid:session_id>/', booth_views.result, name='result'),
    
    # Photo Capture App
    path('photo/', photo_views.capture_ui, name='photo_ui'),
    path('photo/process/', photo_views.process_request, name='photo_process'),
    
    # GIF Capture App
    path('gif/', gif_views.capture_ui, name='gif_ui'),
    path('gif/process/', gif_views.process_request, name='gif_process'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
