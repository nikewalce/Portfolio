from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

'''Метод get_queryset() менеджера возвращает набор запросов QuerySet, который будет исполнен. Мы переопределили этот метод, чтобы сформировать
конкретно-прикладной набор запросов QuerySet, фильтрующий посты по их
статусу и возвращающий поочередный набор запросов QuerySet, содержащий
посты только со статусом PUBLISHED'''
#создание конкретно-прикладного менеджера, чтобы извлекать все посты, имеющие статус PUBLISHED
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    #Менеджер tags позволит добавлять, извлекать и удалять теги из объектов Post
    tags = TaggableManager()
    '''определили перечисляемый класс Status путем подклассирования
класса models.TextChoices. Доступными вариантами статуса поста являются
DRAFT и PUBLISHED. Их соответствующими значениями выступают DF и PB, а их
метками или читаемыми именами являются Draft и Published'''
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    #заголовок поста
    title = models.CharField(max_length=250)
    #короткая метка(при использовании параметра unique_for_date поле slug должно быть уникальным для даты, сохраненной в поле publish)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    '''Это поле определяет взаимосвязь многиек-одному, означающую, что каждый пост написан пользователем и пользователь может написать любое число постов. Для этого поля Django создаст
внешний ключ в базе данных, используя первичный ключ соответствующей
модели.'''
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    #тело поста
    body = models.TextField()
    #хранение даты и времени публикации поста
    publish = models.DateTimeField(default=timezone.now)
    #хранения даты и времени создания поста
    created = models.DateTimeField(auto_now_add=True)
    #хранения последней даты и времени обновления поста(При применении параметра auto_now дата будет обновляться автоматически во время сохранения объекта)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    '''поле status, являющееся экземпляром типа CharField. Оно содержит параметр choices, чтобы ограничивать
значение поля вариантами из Status.choices. Кроме того, применяя параметр
default, задано значение поля, которое будет использоваться по умолчанию'''
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)


    #Мета-класс для сортировки в хронологическом порядке(вверху новые)
    class Meta:
        ordering = ['-publish']
        #индекс по полю publish, а перед именем поля применен дефис, чтобы определить индекс в убывающем порядке
        indexes = [
            models.Index(fields=['-publish']),
        ]

    # Django будет использовать этот метод для отображения имени объекта во многих местах, таких как его сайт администрирования
    def __str__(self):
        return self.title

    #Функция reverse() будет формировать URL-адрес динамически, применяя имя URL-адреса, определенное в шаблонах URL-адресов
    def get_absolute_url(self):
        return reverse('Projects:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
    on_delete=models.CASCADE,
    related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'