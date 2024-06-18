from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Projects.urls', namespace='default')),
    path('Projects/', include('Projects.urls', namespace='Projects')),
]
