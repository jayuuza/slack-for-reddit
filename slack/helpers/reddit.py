class Post(object):
    def __init__(self, post_payload):
        self.kind = post_payload['kind']
        self.data = post_payload['data']
        self.slack_attachment = None

    def make_attachment(self):

        slack_attachment = {
                "fallback": "Reddit post.",
                "title": self.data['title'],
                "title_link": self.data['url'],
                "mrkdwn": True,
            }

        if self.data['selftext']:
            slack_attachment['text'] = self.data['selftext']
        else:
            slack_attachment['text'] = "<https://reddit.com" + self.data['permalink'] + "|View " + str(self.data['num_comments']) + " comments" + ">"

        if self.data['media'] is not None:
            slack_attachment['thumb_url'] = self.data['media']['oembed']['thumbnail_url']
            slack_attachment['image_url'] = self.data['media']['oembed']['thumbnail_url']
        else:
            slack_attachment['thumb_url'] = self.data['thumbnail']
            slack_attachment['image_url'] = self.data['thumbnail']

        self.slack_attachment = slack_attachment

        return slack_attachment


class MessageBuilder(object):
    def __init__(self, message_text, posts):
        self.message = {
            "response_type": "in_channel",
            "text":message_text,
            "attachments": [post.make_attachment() for post in posts],
        }
