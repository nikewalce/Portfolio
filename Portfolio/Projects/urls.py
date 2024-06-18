from django.urls import path
from . import views

#именное пространство приложения
app_name = 'Projects'

urlpatterns = [
    # представления поста
    #Первый шаблон URL-адреса не принимает никаких аргументов и соотносится с представлением post_list
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path("info", views.index),
    #Альтернативное представление списка постов
    #path('', views.PostListView.as_view(), name='post_list'),
    #Второй шаблон соотносится с представлением post_detail и принимает только один аргумент id, который совпадает с целым числом, заданным целым числом конвертора путей int
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]