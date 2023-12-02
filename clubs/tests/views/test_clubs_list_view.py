from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Role
from clubs.tests.helpers import reverse_with_next

class UserListTest(TestCase):

    fixtures = [ 'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_user.json'
                ]

    def setUp(self):
        self.club = Club.objects.get(pk = 1)
        self.user = User.objects.get(pk = 1)
        self.url = reverse('clubs_list')

    def test_user_list_url(self):
        self.assertEqual(self.url, '/clubs_list/')

    def test_get_club_list(self):
        self.client.login(email=self.user.email, password='Password123')
        self._create_test_Club(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clubs_list.html')
        self.assertEqual(len(response.context['clubs']), settings.USERS_PER_PAGE)
        for club_id in range(settings.USERS_PER_PAGE-1):
                self.assertContains(response, f'Club{club_id}')
                self.assertContains(response, f'Location{club_id}')
                self.assertContains(response, f'This is club {club_id}')
                self.assertContains(response, 1)
                club = Club.objects.get(name = f'Club{club_id}')
                club_url = reverse('club_info', kwargs={'club_id':club.id})
                self.assertContains(response, club_url)


    def test_get_user_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_Club(self, user_count=10):
        for club_id in range(user_count):
            club = Club.objects.create(
                name = f'Club{club_id}',
                location =f'Location{club_id}',
                description = f'This is club {club_id}'
            )
            Role.objects.create(club = club, user = self.user, club_role = 'Owner')
