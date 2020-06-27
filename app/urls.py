from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from app import views
from app.views import EventAutocompleteView, EventSearchView

router = DefaultRouter()
router.register(
    'categories', views.CategoriesViewset, basename='categories'
)
router.register(
    'events', views.EventViewset, basename='events'
)


whens_router = routers.NestedSimpleRouter(router, r'events', lookup='event')
whens_router.register(r'whens', views.EventWhenViewset, basename='event-whens')

votes_router = routers.NestedSimpleRouter(whens_router, r'whens', lookup='when')
votes_router.register(r'votes',  views.WhenVotesViewset, basename='when-votes')

subscriptions_router = DefaultRouter()
subscriptions_router.register(
    'subscriptions', views.SubscriptionViewSet, basename='subscription'
)

event_subscriptions_router = routers.NestedSimpleRouter(router, r'events', lookup='event')
event_subscriptions_router.register(r'subscriptions', views.EventSubscriptionViewSet, basename='event-subscriptions')

when_comments_router = routers.NestedSimpleRouter(whens_router, r'whens', lookup='when')
when_comments_router.register(r'comments',  views.WhenCommentsViewSet, basename='when-comments')
urlpatterns = [
    path('events/autocomplete/', EventAutocompleteView.as_view()),
    path('events/search/', EventSearchView.as_view()),
    path('', views.hello ),
    path('', include(router.urls)),
    path('', include(whens_router.urls)),
    path('', include(votes_router.urls)),
    path('', include(when_comments_router.urls)),
    path('', include(subscriptions_router.urls)),
    path('', include(event_subscriptions_router.urls)),
]

