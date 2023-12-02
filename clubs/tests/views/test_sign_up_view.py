"""Tests of the sign up view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from clubs.form import SignUpForm
from clubs.models import User
from clubs.tests.helpers import LogInTester


class SignUpViewTestCase(TestCase, LogInTester):
    """Tests of the sign up view."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@example.org',
            'bio': 'My bio',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'personal_statement': 'Hi I am Jane',
            'chess_Level':'4'
        }
        self.user = User.objects.get(email='joe@example.org')


    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_sign_up(self):
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_succesful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('clubs_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        user = User.objects.get(email = 'janedoe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.username, '@janedoe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.bio, 'My bio')
        self.assertEqual(user.chess_Level, '4')
        self.assertEqual(user.personal_statement, 'Hi I am Jane')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
