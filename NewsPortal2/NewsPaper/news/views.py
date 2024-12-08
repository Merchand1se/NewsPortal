from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Post, Category, Subscriber
from .filters import NewsFilter
from .forms import NewForm, ArticleForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.core.cache import cache
from django.utils.translation import gettext as _


class NewsList(ListView):
    model = Post
    ordering = 'creationDate'
    template_name = 'NewsList.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


class NewDetail(DetailView):
    model = Post
    template_name = 'New.html'
    context_object_name = 'new'
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
        return obj


class create_new(PermissionRequiredMixin, CreateView):
    permission_required = ('news.create_product',)
    form_class = NewForm
    model = Post
    template_name = 'NewsCreate.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        return super().form_valid(form)


class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.new_update',)
    form_class = NewForm
    model = Post
    template_name = 'NewsCreate.html'


class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_new',)
    model = Post
    template_name = 'NewDelete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.article_create',)
    form_class = ArticleForm
    model = Post
    template_name = 'NewsCreate.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.article_edit',)
    form_class = NewForm
    model = Post
    template_name = 'NewsCreate.html'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.article_delete',)
    model = Post
    template_name = 'NewDelete.html'
    success_url = reverse_lazy('news_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(user=request.user, category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk')
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)
