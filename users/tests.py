from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.phone_number, '')
        self.assertEqual(profile.city, '')
        self.assertEqual(profile.state, '')
        self.assertEqual(profile.address, '')

    def test_str_method(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), 'John Doe')


class SignalsTest(TestCase):
    def test_create_user_profile_signal(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe',
        )
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)
