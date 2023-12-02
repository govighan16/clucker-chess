"""Tests of the club registration view."""
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.form import ClubRegisterForm
from clubs.tests.helpers import reverse_with_next


class ClubRegisterViewTestCase(TestCase):
    """Tests of the club registration view."""

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('club_register')
        self.user = User.objects.get(email='joe@example.org')

    def test_club_register_url(self):
        self.assertEqual(self.url,'/club_register/')

    def test_get_club_register(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_register.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ClubRegisterForm))
        self.assertFalse(form.is_bound)

    def test_get_club_register_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
