from django.contrib import admin
from .models import Post, Comment

'''Мы сообщаем сайту администрирования, что модель зарегистрирована на
сайте с использованием конкретно-прикладного класса, который наследует
от ModelAdmin. В этот класс можно вставлять информацию о том, как показывать модель на сайте и как с ней взаимодействовать'''
#Декоратор @admin.register() выполняет ту же функцию, что и функция admin.site.register()
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    #Атрибут list_display позволяет задавать поля модели, которые вы хотите показывать на странице списка объектов администрирования
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    #панель фильтров
    list_filter = ['status', 'created', 'publish', 'author']
    #строка поиска
    search_fields = ['title', 'body']
    #заполнять данные автоматически при добавлении новой записи(в строке slug вставлять title)
    prepopulated_fields = {'slug': ('title',)}
    #поиск авторово по ID
    #raw_id_fields = ['author']
    #навигации по иерархии дат
    date_hierarchy = 'publish'
    #критерии сортировки
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']