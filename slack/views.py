import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from slack.helpers.reddit import Post, MessageBuilder

@csrf_exempt
def slack_router(request):

    # token = request.POST.get('token')
    # if token != settings.SLACK_VERIFICATION_TOKEN:
    #     return HttpResponseBadRequest("Unauthorized Request.")
    #
    command = request.POST.get('command', None)
    command_arguments = request.POST.get('text', None)
    command_arguments = command_arguments.split(" ")
    payload = ""

    # extra_parameters = command_arguments[1:] if len(command_arguments) > 1 else None

    # if command_arguments[0] == "random":
    #     payload = reddit_random(extra_parameters)
    payload = get_subreddit_posts(command_arguments)

    return JsonResponse(payload)

# def reddit_random(location="",extra_parameters=None):

def get_subreddit_posts(command_arguments):
    # Get the location of the subreddit
    location = command_arguments[0] if len(command_arguments) > 0 else "random"
    link = "http://www.reddit.com/r/" + location + "/.json"

    # Get any extra parameters passed along in the command
    extra_parameters = command_arguments[1:] if len(command_arguments) > 1 else None
    num_posts = int(extra_parameters[0]) if extra_parameters is not None else 1

    reddit_data = requests.get(link, headers = {'User-agent': 'Slack-for-reddit'})
    reddit_data = reddit_data.json()['data']['children']

    # Removes any stickied posts that may have been fetched
    posts = []
    for child in reddit_data:
        if not bool(child['data']['stickied']):
            posts.append(Post(child))

    message = MessageBuilder(posts[:num_posts])

    return message.message

    # titles = []
    # for post in reddit_data:
    #     titles.append(post['data']['title'])
    #
    # return ", ".join(titles)