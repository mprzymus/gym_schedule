from app.const import COACH_GROUP


def is_coach(user):
    return COACH_GROUP in map(lambda group: group.name, user.groups.filter(name=COACH_GROUP))
