from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'creationDate'
    template_name = 'NewsList.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_new'] = None
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'New.html'
    context_object_name = 'new'


