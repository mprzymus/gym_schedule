from django.contrib.auth.models import User, Group
from django.test import TestCase

from app.model.models import UsersCoach
from app.service.coach_service import *


class MyTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('testUser', 'test@test.com', 'testpass')
        self.coach = User.objects.create_user('coach', 'coach@test.com', 'testpass')
        self.coach_group = Group(name=COACH_GROUP)
        self.coach_group.save()
        self.coach.groups.add(self.coach_group)
        self.coach.save()

    def test_save_group_test(self):
        request_coach(self.user)
        result = UsersCoach.objects.filter(user=self.user)

        self.assertEqual(1, len(result))
        relation = result[0]

        self.assertEqual(self.user, relation.user)
        self.assertEqual(None, relation.coach)

    def test_assign_coach(self):
        relation = request_coach(self.user)

        assign_coach(relation, self.coach)

        coach_users = UsersCoach.objects.filter(coach=self.coach)
        self.assertEqual(1, len(coach_users))
        self.assertEqual(self.user, coach_users[0].user)
        self.assertEqual(self.coach, get_coach_mail(self.user))

    def test_has_not_coach_assigned(self):
        self.assertFalse(did_request_coach(self.user))

    def test_has_coach_assigned(self):
        request_coach(self.user)
        self.assertTrue(did_request_coach(self.user))

    def test_get_coach_no_coach(self):
        request_coach(self.user)

        self.assertEqual(None, get_coach_mail(self.user))

    def test_get_coach_no_request(self):
        self.assertEqual(None, get_coach_mail(self.user))
