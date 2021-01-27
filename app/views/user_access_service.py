from app.service.coach_service import is_coach


def can_user_perform(user, usr_id):
    return user.id == usr_id or is_coach(user)
