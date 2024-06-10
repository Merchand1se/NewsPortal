import logging
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.views.decorators.csrf import csrf_protect
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string

from news.models import Post, Subscriber, Category

logger = logging.getLogger(__name__)

@login_required
@csrf_protect
def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=30)
    posts = Post.objects.filter(dateCreation__gte=last_week).order_by('-dateCreation')
    categories = set(posts.values_list('category__name', flat=True))
    subscribers_emails = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    # print(today)
    # print(f'Статьи за неделю')
    # print(f'Статьи: {posts}')
    # print(f'Категории: {categories}')
    # print(f'Список email подписчиков: {subscribers_emails}')

    for subscriber in subscribers_emails:
        subject = 'Статьи за неделю!!!',
        text_content = render_to_string(
            'post/deily_post.html',
            {
                'link': settings.SITE_URL,
                'posts': posts,
            }
        )
        html_content = render_to_string(
            'post/deily_post.html',
            {
                'link': settings.SITE_URL,
                'posts': posts,
            }
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [subscriber])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")