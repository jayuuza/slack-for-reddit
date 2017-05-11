from django.db import models


# Create your models here.
class Team(models.Model):
    team_id = models.CharField(max_length=200, db_index=True, unique=True)
    team_name = models.CharField(max_length=200, db_index=True)
    access_token = models.CharField(max_length=256, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name


class UsageLog(models.Model):
    team = models.ForeignKey("Team")
    user_id = models.CharField(max_length=200)
    reddit_url = models.CharField(max_length=200)
    slash_command = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
