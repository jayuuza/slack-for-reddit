from accounts.models import Team


def create_team(request, api_data):
    try:
        team = Team.objects.get(team_id=api_data['team_id'])
    except Team.DoesNotExist:
        team = Team(
            access_token=api_data['access_token'],
            team_name=api_data['team_name'],
            team_id=api_data['team_id']
        )

        team.save()
    return request, api_data
