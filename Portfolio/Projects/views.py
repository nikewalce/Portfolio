from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Comment
from django.views.generic import ListView
#Постраничная разбивка
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
#агрегированный подсчет тегов
from django.db.models import Count

def post_list(request, tag_slug=None):
    #В данном представлении извлекаются все посты со статусом PUBLISHED, используя менеджер published
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    #Если параметра page нет в GET-параметрах запроса, то мы используем стандартное значение 1, чтобы загрузить первую страницу результатов
    page_number = request.GET.get('page', 1)
    #обработка исключений при несуществующем номере страницы
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    #Наконец, мы используем функцию сокращенного доступа1 render(), предоставляемую Django, чтобы прорисовать список постов заданным шаблоном
    return render(request, 'Projects/post/list.html', {'posts': posts, 'tag': tag})

# представление детальной информации о посте
def post_detail(request, year, month, day, post):
    '''Указанное представление принимает аргумент id поста. Здесь мы пытаемся извлечь объект Post
с заданным id, вызвав метод get() стандартного менеджера objects. Мы
создаем исключение Http404, чтобы вернуть ошибку HTTP с кодом состояния, равным 404, если возникает исключение DoesNotExist, то есть модель не
существует, поскольку результат не найден.
Наконец, мы используем функцию сокращенного доступа render(), чтобы
прорисовать извлеченный пост с использованием шаблона'''
    #Указанная функция извлекает объект, соответствующий переданным параметрам, либо исключение HTTP с кодом состояния, равным 404 (не найдено), если объект не найден
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментирования пользователями
    form = CommentForm()

    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
                                .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                                .order_by('-same_tags', '-publish')[:4]

    return render(request,
        'Projects/post/detail.html',
        {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """
    #конкретно-прикладной набор запросов QuerySet, не извлекая все объекты
    queryset = Post.published.all()
    #результатов запроса
    context_object_name = 'posts'
    #постраничная разбивка результатов с возвратом трех объектов на страницу
    paginate_by = 3
    ''''конкретно-прикладной шаблон используется для прорисовки страницы
шаблоном template_name. Если шаблон не задан, то по умолчанию ListView будет использовать blog/post_list.html'''
    template_name = 'Projects/post/list.html'

def post_share(request, post_id):
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post,
                            id=post_id,
                            status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'nikewalce1@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'Projects/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST
def post_comment(request, post_id):
    #По id поста извлекается опубликованный пост, используя функцию сокращенного доступа get_object_or_404()
    post = get_object_or_404(Post,
    id=post_id,
    status=Post.Status.PUBLISHED)
    #Указанная переменная будет использоваться для хранения комментарного объекта при его создании.
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    #Если форма невалидна, то шаблон прорисовывается с ошибками валидации
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'Projects/post/comment.html',
                            {'post': post,
                                'form': form,
                                'comment': comment})



def index(request):
    host = request.META["HTTP_HOST"]  # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]  # получаем данные бразера
    path = request.path  # получаем запрошенный путь
    return render(request, 'Projects/post/info.html', {'host': host,
                                                    'user_agent': user_agent,
                                                    'path': path})
# def index(request):
#     return HttpResponse("Projects")
