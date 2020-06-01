from django.contrib import admin

# Register your models here.
from app.models import Event, Subscription, Category, Comment, Vote, When, WhenComment

admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Subscription)
admin.site.register(Vote)
admin.site.register(When)
admin.site.register(WhenComment)