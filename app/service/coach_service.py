from django.contrib.auth.models import User

from app.const import COACH_GROUP
from app.model.models import UsersCoach


def find_all_coaches():
    User.objects.filter(group_name=COACH_GROUP)


def request_coach(user):
    relation = UsersCoach()
    relation.user = user
    relation.save()
    return relation


def assign_coach(coach_user: UsersCoach, coach):
    coach_user.coach = coach
    coach_user.save()
    return coach_user


def did_request_coach(user):
    return len(UsersCoach.objects.filter(user=user)) != 0