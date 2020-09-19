from django.http import JsonResponse
from app.views.categories import CategoriesViewset
from app.views.events import EventAutocompleteView, EventSearchView, EventViewSet, SubmittedEventsView
from app.views.whens import *
from app.views.when_comments import *
from app.views.comments import *
from app.views.votes import *
from app.views.subscriptions import *

def hello(request):
    return JsonResponse({
        "version": "0.0"
    })



