from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Post
from .filters import NewsFilter
from .forms import NewForm, ArticleForm
from django.urls import reverse_lazy


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


class create_new(CreateView):
    form_class = NewForm
    model = Post
    template_name = 'NewsCreate.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        return super().form_valid(form)


class NewUpdate(UpdateView):
    form_class = NewForm
    model = Post
    template_name = 'NewsCreate.html'


class NewDelete(DeleteView):
    model = Post
    template_name = 'NewDelete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'NewsCreate.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = NewForm
    model = Post
    template_name = 'NewsCreate.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'NewDelete.html'
    success_url = reverse_lazy('news_list')