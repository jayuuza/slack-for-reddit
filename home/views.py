from django.shortcuts import render
from django.conf import settings


def index(request):
    client_id = settings.SLACK_CLIENT_ID
    return render(request, 'home/index.html', {'client_id': client_id})
