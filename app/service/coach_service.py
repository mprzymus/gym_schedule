from app.const import COACH_GROUP


def is_coach(user):
    print(user.groups.filter(name=COACH_GROUP))
    return COACH_GROUP in map(lambda group: group.name, user.groups.filter(name=COACH_GROUP))
