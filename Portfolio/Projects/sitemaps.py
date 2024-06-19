from django.contrib.sitemaps import Sitemap
from .models import Post

'''Мы определили конкретно-прикладную карту сайта, унаследовав класс
Sitemap модуля sitemaps. Атрибуты changefreq и priority указывают частоту
изменения страниц постов и их релевантность на веб-сайте (максимальное
значение равно 1).'''
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated