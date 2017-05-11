from accounts.models import Team


def create_team(request, api_data):
    team = Team.objects.get(team_id=api_data['team_id'])
    if not team:
        team = Team(
            access_token=api_data['access_token'],
            team_name=api_data['team_name'],
            team_id=api_data['team_id']
        )

        team.save()
    return request, api_data
