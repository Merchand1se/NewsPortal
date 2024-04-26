from django.views.generic import ListView, DetailView
from .models import Post



class NewsList(ListView):
    model = Post
    ordering = 'creationDate'
    template_name = 'NewsList.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'New.html'
    context_object_name = 'new'


