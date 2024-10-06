from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from .models import Post


@receiver(m2m_changed, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriber__category=instance.category
    ).value_list('email', flat=True)

    subject = f'There is something new happened in {instance.category}'

    text_content = (
        f'Title: {instance.title}\n'
        f'Date: {instance.date}\n\n'
        f'Read more: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content= (
        f'Title: {instance.title}<br>'
        f'Date: {instance.date}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Read more</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()