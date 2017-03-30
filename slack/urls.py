from django.conf.urls import url
from slack.views import slack_router

urlpatterns = [
    url(r'^$', slack_router, name='slack'),
]

