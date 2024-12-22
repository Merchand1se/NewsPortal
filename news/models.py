from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


class Author(models.Model):
    autUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAut = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_sum = self.post_set.aggregate(postRating=Sum('rating'))
        temp_sum_p = 0
        temp_sum_p += post_sum.get('postRating')
        comment_sum = self.autUser.comment_set.aggregate(commentRating=Sum('rating'))
        temp_sum_c = 0
        temp_sum_c += comment_sum.get('commentRating')

        self.ratingAut = temp_sum_p * 3 + temp_sum_c
        self.save()

class Category(models.Model):
    name = models.CharField(_('Category name'),max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGOY_CHOICES = (
        ('AR', 'Статья'),
        ('NW', 'Новость'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(_('Type'), max_length=2,choices=CATEGOY_CHOICES, default=ARTICLE)
    creationDate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(_('Title'), max_length=100)
    content = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:123]} ...'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}cd ')


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscriber(models.Model):
    user=models.ForeignKey(
    to=User,
    on_delete=models.CASCADE,
    related_name='subscription',
    )
    catergory=models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscription'
    )

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='kinds',
        verbose_name=pgettext_lazy('help text for MyModel model', 'This is the help text'),
    )


