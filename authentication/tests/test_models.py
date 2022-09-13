from authentication.models import User
from django.test import TestCase

class TestModels(TestCase):

    def test_should_create_user(self):
        user = User.objects.create_user(username='opiyox',email="opiyo@g.n")
        user.set_password("Opandex")
        user.save()

        self.assertEqual(str(user),'opiyo@g.n')