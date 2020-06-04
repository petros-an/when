from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.contrib.auth.models import User
from django.db.models import CheckConstraint, Q, UniqueConstraint


class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.CharField(max_length=30, db_index=True, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Event(models.Model):
    status_choices = (
        ('accepted', 'Accepted'),
        ('flagged', 'Accepted'),
        ('deleted', 'Accepted')
    )

    title = models.CharField(max_length=120)
    description = models.TextField()
    info = JSONField(default=dict, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    prevalent_when = models.ForeignKey(to="When", on_delete=models.CASCADE, related_name="prevalent_when", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=True, to_field="slug")
    status = models.CharField(max_length=50, choices=status_choices, default='accepted')

    class Meta:
        indexes = [
            GinIndex(fields=["title", "description"])
        ]


    def __str__(self):
        return self.title



class Subscription(models.Model):
    SUBSCRIPTION_CHOICES = (
        ('email', 'Email'),
    )

    default_subscription_config = {}
    user = models.ForeignKey(to=User, related_name='user_subscriptions', on_delete=models.CASCADE)
    config = JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(to=Event, related_name='event_subscriptions', on_delete=models.CASCADE)
    method = models.CharField(max_length=100, choices=SUBSCRIPTION_CHOICES)

    def __str__(self):
        return f"{self.user.username} is subscribed to {self.event.title} "


class Comment(models.Model):
    text = models.TextField()
    event = models.ForeignKey(to=Event, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class WhenComment(models.Model):
    text = models.TextField()
    when = models.ForeignKey(to="When", related_name='when_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)


class Vote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    when = models.ForeignKey(to="When", related_name='votes', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        verb = "Approves"
        return f"User {self.user_id} {verb} {str(self.when)}"


class When(models.Model):
    confidence_choices = (
        ('certainly', 'Certainly'),
        ('probably', 'Probably'),
        ('maybe', 'Maybe')
    )

    status_choices = (
        ('accepted', 'Accepted'),
        ('flagged', 'Accepted'),
        ('deleted', 'Accepted')
    )

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.TextField()
    event = models.ForeignKey(to=Event, related_name='whens', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    sources = ArrayField(default=list, base_field=models.URLField(), blank=True)
    score = models.FloatField(default=0)
    chosen = models.BooleanField(default=False)
    confidence = models.CharField(max_length=40, choices=confidence_choices, default='probably')
    status = models.CharField(max_length=50, choices=status_choices, default='accepted')
    when = models.DateTimeField()



    def __str__(self):
        return f"{self.event.title} : {self.confidence} on {self.when.__str__()} - {self.score}"


class NotificationAttempt(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subscription = models.ForeignKey(to=Subscription, on_delete=models.CASCADE)
    result = JSONField(default=dict, blank=True)
    delta_days = models.IntegerField()

    def __str__(self):
        return f"Notified {self.subscription.user.username} for {self.subscription.event.title} at {self.created}"

class PowerUser(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)