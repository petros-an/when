from datetime import timedelta
import logging
from app.celery import app as celery_app
from django.utils import timezone

log = logging.getLogger(__name__)

from app.models import Item, Subscription, NotificationAttempt, Proposition

SUBSCRIPTION_TIMEDELTAS = {
    '1day': timedelta(days=1),
    '3days': timedelta(days=3),
    '1week': timedelta(days=7),
    '2weeks': timedelta(days=14),
    '1month': timedelta(days=30),
    '2months': timedelta(days=60),
    '4months': timedelta(days=120),
}

@celery_app.task
def initiate_due_notifications_for_all_deltas():
    for delta_name, delta_value in SUBSCRIPTION_TIMEDELTAS.items():
        initiate_due_notifications_for_delta.apply_async((delta_name,))

@celery_app.task
def initiate_due_notifications_for_delta(delta_name):
    delta_value = SUBSCRIPTION_TIMEDELTAS[delta_name]
    whens_due = Proposition.objects.prefetch_related("prevalent_when").filter(
        when__lte=timezone.now() + delta_value,
        when__gte=timezone.now()
    )
    for when in whens_due:
        subscriptions = when.item.event_subscriptions.filter(
            config__has_key=delta_name
        )
        for subscription in subscriptions:
            notify_subscription_for_delta.apply_async((subscription.id, delta_name))


@celery_app.task
def notify_subscription_for_delta(subscription_id, delta_name):
    delta = SUBSCRIPTION_TIMEDELTAS[delta_name]
    try:
        subscription = Subscription.objects.get(id=subscription_id)
    except Subscription.DoesNotExist:
        raise AssertionError("Invalid notification details: Subscription object not found")
    if subscription.method == "email":
        if NotificationAttempt.objects.filter(
            subscription=subscription,
            delta_days=delta.days
        ).exists():
            return
        result = notify_by_email(subscription)
        NotificationAttempt.objects.get_or_create(
            subscription=subscription,
            delta_days=delta.days,
            method='email'
        )
    else:
        raise NotImplementedError("Notification method not implemented")

def initiate_notifications_for_prevalent_when_change(event_id):
    event = Item.objects.select_related("prevalent_when").get(id=event_id)
    for subscription in event.subscriptions.filter(config__notify_on_change=True):
        notify_by_email(subscription)


def notify_by_email(subscription):
    log.info(f"Sending email for {str(subscription)}")
