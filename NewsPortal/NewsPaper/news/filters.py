from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Category

class NewsFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='Category',
        queryset=Category.objects.all()
    )
    class Meta:
        model=Post
        fields = {
            'Name':['icontains'],
            'After date':['gt'],
        }