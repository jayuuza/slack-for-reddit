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
    command_arguments = request.POST.get('text', None)
    command_arguments = command_arguments.split()
    payload = get_subreddit_posts(command_arguments)

    return JsonResponse(payload)

def get_subreddit_posts(command_arguments):

    no_arguments = len(command_arguments)

    # Get the location of the subreddit
    location = command_arguments[0] if no_arguments > 0 else "random"

    # Get the specific listing of the subreddit
    # Examples: controversial, hot, new, random, rising, top, sort
    # Additional sorting and filtering commands available only on listings
    # They are: before / after, count, limit, show
    # news
    # news 10 or 10 news
    # news 10 top or news/top 10
    # More info can be viewed here: https://www.reddit.com/dev/api/#listings

    #listing = "/" + command_arguments[1] if no_arguments > 1 else  ""
    #filters = "?" + command_arguments[2] if no_arguments > 2 else ""


    link = "http://www.reddit.com/r/" + location + ".json"

    # Fetch the reddit data
    reddit_data = requests.get(link, headers = {'User-agent': 'Slack-for-reddit'})
    reddit_data = reddit_data.json()['data']['children']

    # Get any extra parameters passed along in the command
    extra_parameters = command_arguments[1:] if len(command_arguments) > 1 else None
    num_posts = int(extra_parameters[0]) if extra_parameters is not None else 1

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