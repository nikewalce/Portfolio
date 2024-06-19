import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

#новостная лента
class LatestPostsFeed(Feed):
    title = 'My Project'
    #генерировать URL-адрес для атрибута link
    link = reverse_lazy('Projects:post_list')
    description = 'New posts of my project.'

    #извлекает включаемые в новостную ленту объекты
    def items(self):
        return Post.published.all()[:5]

    #возвращать заголовок по каждому элементу
    def item_title(self, item):
        return item.title

    #возвращать описание по каждому элементу
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    #возвращать дату публикации по каждому элементу
    def item_pubdate(self, item):
        return item.publish