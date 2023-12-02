from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Role
from clubs.tests.helpers import reverse_with_next

class UserListTest(TestCase):

    fixtures = [ 'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json',
                ]

    def setUp(self):
        self.club = Club.objects.get(pk = 1)
        self.user = User.objects.get(pk = 1)
        self.owner = User.objects.get(pk = 2)
        self.url = reverse('club_info', kwargs={'club_id':self.club.id})
        self.role = Role.objects.create(club=self.club, user = self.owner, club_role = 'Owner')

    def test_show_user_in_No_role_url(self):
        role = Role.objects.create(club=self.club, user = self.user, club_role = 'No role')
        self.assertEqual(self.url, f'/club/{self.club.id}')

    def test_get_club_info_for_No_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_info.html')
        self.assertContains(response, 'London Club')
        self.assertContains(response, 'London')
        self.assertContains(response, 'The Official London Chess Club')
        self.assertContains(response, '0')
        user = User.objects.get(email='joe@example.org')
        role = Role.objects.get(club = self.club, user = user)
        apply_url = reverse('applyUser', kwargs={'role_id':role.id})
        #self.assertContains(response, apply_url)

    def test_show_user_in_Owner_role_url(self):
        role = Role.objects.create(club=self.club, user = self.user, club_role = 'Owner')
        self.assertEqual(self.url, f'/club/{self.club.id}')

    def test_get_club_info_for_Owner_Role(self):
        role = Role.objects.create(club=self.club, user = self.user, club_role = 'Member')
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_info.html')
        self.assertContains(response, 'London Club')
        self.assertContains(response, 'London')
        self.assertContains(response, 'The Official London Chess Club')
        self.assertContains(response, '0')
        self.assertContains(response, 'Owner')
        list_url = reverse('list', kwargs={'club_id':self.club.id} )
        self.assertContains(response, list_url)

    def test_show_user_in_Officer_role_url(self):
        role = Role.objects.create(club=self.club, user = self.user, club_role = 'Officer')
        self.assertEqual(self.url, f'/club/{self.club.id}')

    def test_get_club_info_for_Officer_Role(self):
        role = Role.objects.create(club=self.club, user = self.user, club_role = 'Officer')
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_info.html')
        self.assertContains(response, 'London Club')
        self.assertContains(response, 'London')
        self.assertContains(response, 'The Official London Chess Club')
        self.assertContains(response, '0')
        self.assertContains(response, 'Officer')
        list_url = reverse('list', kwargs={'club_id':self.club.id} )

    def test_show_user_in_Member_role_url(self):
        role = Role.objects.create(club=self.club, user = self.user, club_role = 'Member')
        self.assertEqual(self.url, f'/club/{self.club.id}')

    def test_get_club_info_for_Member_Role(self):
        role = Role.objects.create(club=self.club, user = self.user, club_role = 'Member')
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_info.html')
        self.assertContains(response, 'London Club')
        self.assertContains(response, 'London')
        self.assertContains(response, 'The Official London Chess Club')
        self.assertContains(response, '0')
        self.assertContains(response, 'Member')
        list_url = reverse('list', kwargs={'club_id':self.club.id} )

    def test_show_user_in_Applicant_role_url(self):
        role = Role.objects.create(club=self.club, user = self.user, club_role = 'Applicant')
        self.assertEqual(self.url, f'/club/{self.club.id}')

    def test_get_club_info_for_Applicant_Role(self):
        role = Role.objects.create(club=self.club, user = self.user, club_role = 'Applicant')
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_info.html')
        self.assertContains(response, 'London Club')
        self.assertContains(response, 'London')
        self.assertContains(response, 'The Official London Chess Club')
        self.assertContains(response, '0')
        self.assertContains(response, 'Applicant')
        list_url = reverse('list', kwargs={'club_id':self.club.id} )
