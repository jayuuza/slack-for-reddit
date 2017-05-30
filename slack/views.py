import requests
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import UsageLog, Team
import html

from slack.helpers.reddit import Post, MessageBuilder


@csrf_exempt
def slack_router(request):
    token = request.POST.get('token')
    if token != settings.SLACK_VERIFICATION_TOKEN:
        return HttpResponseBadRequest("Unauthorized Request.")

    command = request.POST.get('command')
    command_arguments = html.escape(request.POST.get('text', None))
    command_arguments = command_arguments.split()
    subreddit, payload = get_subreddit_posts(command, command_arguments)

    log_usage(request, subreddit)

    return JsonResponse(payload)


def log_usage(request, subreddit):
    t_id = request.POST.get('team_id')
    team = Team.objects.get(team_id=t_id)

    log = UsageLog(
        team=team,
        user_id=request.POST.get('user_id'),
        reddit_url=subreddit,
        slash_command=request.POST.get('command') + ' ' + request.POST.get('text', None),
    )

    log.save()


def get_subreddit_posts(command, command_arguments):
    no_arguments = len(command_arguments)

    location = "r/random"
    num_posts = 1

    # Get the location of the subreddit
    if command == "/slackrd":
        if no_arguments == 1:
            location = "r/" + command_arguments[0] if not command_arguments[0].isdigit() else ""
            num_posts = int(command_arguments[0]) if command_arguments[0].isdigit() else 1
        elif no_arguments > 1:
            location = "r/" + command_arguments[1] if not command_arguments[1].isdigit() else ""
            num_posts = int(command_arguments[0]) if command_arguments[0].isdigit() else 1
        else:
            location = ""
            num_posts = 1

    if num_posts > 10:
        num_posts = 10

    # Get the specific listing of the subreddit
    # Examples: controversial, hot, new, random, rising, top, sort
    # Additional sorting and filtering commands available only on listings
    # They are: before / after, count, limit, show
    # More info can be viewed here: https://www.reddit.com/dev/api/#listings
    link = "http://www.reddit.com/" + location + ".json"

    # Fetch the reddit data
    reddit_data = requests.get(link, headers={'User-agent': 'Slack-for-reddit'})
    reddit_data = reddit_data.json()['data']['children']
    subreddit = "http://www.reddit.com/r/" + reddit_data[0]['data']['subreddit']

    if num_posts > 1:
        message_text = str(num_posts) + " posts from " + subreddit
    else:
        message_text = "Post from " + subreddit

    # Removes any stickied posts that may have been fetched
    posts = []
    for child in reddit_data:
        if not bool(child['data']['stickied']):
            posts.append(Post(child))

    message = MessageBuilder(message_text, posts[:num_posts])

    return subreddit, message.message