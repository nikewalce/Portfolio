from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
import Projects.sitemaps

sitemaps = {
'posts': Projects.sitemaps.PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Projects.urls', namespace='default')),
    path('Projects/', include('Projects.urls', namespace='Projects')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]
