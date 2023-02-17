from django.test import TestCase
from model_bakery import baker

from accounts.models import User


class TestUser(TestCase):
    def test_model_user(self):
        user = User.objects.create(first_name='sara', last_name='ahmdi')
        self.assertEqual(str(user), 'sara-ahmadi')

    def test_create_user(self):
        user = baker.make(User, first_name='mona', last_name='asadi')
        self.assertEqual(str(user), 'mona-asadi')

