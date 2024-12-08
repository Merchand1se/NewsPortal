import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper.NewsPaper import settings
from .models import Post

@shared_task
def new_mess(preview, pk, title, subscribers):
    html_content = render_to_string(
    'post/email_new_post.html',
    {
        'text': preview,
        'link': f'{settings.SITE_URL}/post/{pk}',
    },
)

    msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html_content, "text/html")
    msg.send()




@shared_task
def weekly_news_report():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week).order_by('-dateCreation')
    categories = []
    subscribers = []
    for post in posts:
        categories += [cat for cat in post.category.all()]
    for category in categories:
        subscribers += [sub for sub in category.subscribers.all()]
    for subscriber in subscribers:
        subject = 'Статьи за неделю!!!'
        text_content = render_to_string(
            'post/email_weekly_post.html',
            {
                'username': subscriber.username,
                'link': settings.SITE_URL,
                'posts': posts,
            },
        )
        html_content = render_to_string(
            'post/email_weekly_post.html',
            {
                'link': settings.SITE_URL,
                'posts': posts,
            },
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

