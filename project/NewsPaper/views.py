from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.views import View

from .models import Post
from .filters import PostFilter
from .forms import PostForm, UserForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-datetime')
    # ordering = ['-price']
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())

        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class SearchNews(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-datetime')

    # paginate_by = 1

    def get(self, request):
        post_list = Post.objects.all()  # получаем все публикации
        # создаем объект фильтра
        post_filter = PostFilter(request.GET, queryset=post_list)
        post_list = post_filter.qs  # создаем переменную с QuerySet фильтра
        # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
        paginator = Paginator(post_list, 5)
        # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
        page = request.GET.get('page', 1)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        args = {'paginator': paginator, 'filter': post_filter, 'posts': posts}

        return render(request, 'search.html', args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())
        return context

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostDetail(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()


class PostCreateView(CreateView):
    template_name = 'post_add.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'post_add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    form_class = UserForm

    def get_object(self, **kwargs):
        id = self.request.user.id
        return User.objects.get(pk=id)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
