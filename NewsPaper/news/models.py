from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    autUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAut = models.IntegerField(default=0)

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
    name = models.CharField(unique=True, max_length=255)



class Post(models.Model):
    Article = "AR"
    News = "NW"
    CategoryChoice = [
        ('AR', 'Статья'),
        ('NW', 'Новость'),
    ]

    author = models.OneToOneField(Author, on_delete=models.CASCADE),
    ArticleNewCategory = models.CharField(choices=CategoryChoice, default=News),
    CreateDate = models.DateTimeField(auto_now_add=True),
    PostInfo = models.ManyToManyField(Category, through='PostCategory'),
    Heading = models.CharField(max_length=100),
    Content = models.TextField(),
    rating = models.IntegerField(default=0)

    def Preview(self):
        return f'{self.Content[:123]} ...'

class PostCategory:
    post = models.ForeignKey(Post, on_delete=models.CASCADE),
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE),
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CommentContent = models.TextField(),
    Date = models.DateTimeField(auto_now_add=True),
    rating = models.IntegerField(default=0)

    def Like(self):
        self.rating += 1
        self.save()

    def Dislike(self):
        self.rating -= 1
        self.save()

