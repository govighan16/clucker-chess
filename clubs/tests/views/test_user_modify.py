"""Tests of the club registration view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Role
from clubs.form import ProfileForm
from clubs.tests.helpers import reverse_with_next
from django.contrib import messages


class ClubRegisterViewTestCase(TestCase):
    """Tests of the club registration view."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('profile')
        self.user = User.objects.get(email='joe@example.org')
        self.form_input = {
            'first_name': 'Joe2',
            'last_name': 'Doe2',
            'username': '@joedoe2',
            'email': 'joe@email.org',
            'bio': 'New bio',
            'chess_Level':3,
            'personal_statement':'Hi i am Joe2',
        }


    def test_profile_url(self):
        self.assertEqual(self.url,'/profile/')

    def test_get_profile(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ProfileForm))
        self.assertFalse(form.is_bound)

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccesful_profile_update(self):
        self.client.login(username=self.user.email, password='Password123')
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ProfileForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@joedoe')
        self.assertEqual(self.user.first_name, 'Joe')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'joe@example.org')
        self.assertEqual(self.user.bio, "My bio")
        self.assertEqual(self.user.chess_Level, '4')
        self.assertEqual(self.user.personal_statement, "Hi I am Joe")

    def test_unsuccessful_profile_update_due_to_informat_username(self):
        self.client.login(username=self.user.email, password='Password123')
        self.form_input['username'] = 'joedoe'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ProfileForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@joedoe')
        self.assertEqual(self.user.first_name, 'Joe')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'joe@example.org')
        self.assertEqual(self.user.bio, "My bio")
        self.assertEqual(self.user.chess_Level, '4')
        self.assertEqual(self.user.personal_statement, "Hi I am Joe")

    def test_succesful_profile_update(self):
        self.client.login(username=self.user.email, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@joedoe2')
        self.assertEqual(self.user.first_name, 'Joe2')
        self.assertEqual(self.user.last_name, 'Doe2')
        self.assertEqual(self.user.email, 'joe@email.org')
        self.assertEqual(self.user.bio, 'New bio')
        self.assertEqual(self.user.chess_Level, '3')
        self.assertEqual(self.user.personal_statement, "Hi i am Joe2")
