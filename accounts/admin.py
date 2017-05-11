from django.contrib import admin

# Register your models here.
from accounts.models import UsageLog
from accounts.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["id","team_id","team_name","created"]
    search_fields = ["team_name"]
    list_filter = ["created"]


@admin.register(UsageLog)
class UsageLogAdmin(admin.ModelAdmin):
    list_display = ["id", "team", "slash_command", "created"]
    search_fields = []
    list_filter = ["created"]
