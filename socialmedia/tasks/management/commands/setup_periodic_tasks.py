from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import get_default_timezone_name

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask
from socialmedia.users.tasks import profile_update as profile_update_task



class Command(BaseCommand):
    help = f"""
    Setup celery beat periodic tasks.

    Following tasks will be created:

    - ....
    """

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print('Deleting all periodic tasks and schedules...\n')

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            {
                'task': profile_update_task,
                'name': 'Do some peridoic stuff',
                'cron': {
                    'minute': '*',
                    'hour': '*',
                    'day_of_week': '*',
                    'day_of_month': '*',
                    'month_of_year': '*',
                },
                'enabled': True
            },
        ]

        for periodic_task in periodic_tasks_data:
            print(f'Setting up {periodic_task["task"].name}')

            cron = CrontabSchedule.objects.create(
                **periodic_task['cron']
            )

            PeriodicTask.objects.create(
                name=periodic_task['name'],
                task=periodic_task['task'].name,
                crontab=cron,
                enabled=periodic_task['enabled']
            )