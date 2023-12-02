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

        self.url = reverse('list', kwargs={'club_id':self.club.id})

    def test_user_list_url(self):
        self.assertEqual(self.url,f'/list/{self.club.id}')

    def test_get_Member_list_for_Member_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        self.role = Role.objects.create(user=self.user, club=self.club, club_role = 'Member')
        self._create_test_Member(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        for user_id in range(settings.USERS_PER_PAGE-1):
            if user_id %2 == 0:
                self.assertContains(response, f'@user{user_id}')
                self.assertContains(response, f'First{user_id}')
                self.assertContains(response, f'Last{user_id}')
                user = User.objects.get(email=f'user{user_id}@test.org')


    def test_get_list_for_Applicant_Role_without_applicant(self):
        self.client.login(email=self.user.email, password='Password123')
        self.role = Role.objects.create(user=self.user, club=self.club, club_role = 'Applicant')
        self._create_test_Member(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(len(response.context['users']), 1)

    def test_get_list_for_Owner_Role_without_applicant(self):
        self.client.login(email=self.user.email, password='Password123')
        self.role = Role.objects.create(user=self.user, club=self.club, club_role = 'Owner')
        self._create_test_Member(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        for user_id in range(settings.USERS_PER_PAGE-1):
            self.assertContains(response, f'@user{user_id}')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'user{user_id}@test.org')
            user = User.objects.get(email=f'user{user_id}@test.org')
            user_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id': user.id})
            self.assertContains(response, user_url)

    def test_get_list_for_Officer_Role_without_applicant(self):
        self.client.login(email=self.user.email, password='Password123')
        self.role = Role.objects.create(user=self.user, club=self.club, club_role = 'Officer')
        self._create_test_Member(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        for user_id in range(settings.USERS_PER_PAGE-1):
            self.assertContains(response, f'@user{user_id}')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'user{user_id}@test.org')
            user = User.objects.get(email=f'user{user_id}@test.org')
            user_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id': user.id})
            self.assertContains(response, user_url)

    def test_get_list_for_Member_Role_without_applicant(self):
        self.client.login(email=self.user.email, password='Password123')
        self.role = Role.objects.create(user=self.user, club=self.club, club_role = 'Member')
        self._create_test_Member(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        for user_id in range(settings.USERS_PER_PAGE-1):
            self.assertContains(response, f'@user{user_id}')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            user = User.objects.get(email=f'user{user_id}@test.org')

    def test_get_list_for_Applicant_Role_with_applicant(self):
        self.client.login(email=self.user.email, password='Password123')
        self.role = Role.objects.create(user=self.user, club=self.club, club_role = 'Applicant')
        self._create_test_Applicant(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE/2)
        for user_id in range(settings.USERS_PER_PAGE-1):
            if user_id %2 != 0:
                self.assertContains(response, f'@user{user_id}')
                self.assertContains(response, f'First{user_id}')
                self.assertContains(response, f'Last{user_id}')
                user = User.objects.get(email=f'user{user_id}@test.org')

    def test_get_list_for_Member_Role_with_applicant(self):
        self.client.login(email=self.user.email, password='Password123')
        self.role = Role.objects.create(user=self.user, club=self.club, club_role = 'Member')
        self._create_test_Applicant(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(len(response.context['users']), (settings.USERS_PER_PAGE/2)+1)
        for user_id in range(settings.USERS_PER_PAGE-1):
            if user_id %2 == 0:
                self.assertContains(response, f'@user{user_id}')
                self.assertContains(response, f'First{user_id}')
                self.assertContains(response, f'Last{user_id}')
                user = User.objects.get(email=f'user{user_id}@test.org')

    def test_get_list_for_Officer_Role_with_applicant(self):
        self.client.login(email=self.user.email, password='Password123')
        self.role = Role.objects.create(user=self.user, club=self.club, club_role = 'Officer')
        self._create_test_Applicant(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        for user_id in range(settings.USERS_PER_PAGE-1):
            self.assertContains(response, f'@user{user_id}')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'user{user_id}@test.org')
            user = User.objects.get(email=f'user{user_id}@test.org')
            user_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id': user.id})
            self.assertContains(response, user_url)

    def test_get_list_for_Owner_Role_with_applicant(self):
        self.client.login(email=self.user.email, password='Password123')
        self.role = Role.objects.create(user=self.user, club=self.club, club_role = 'Owner')
        self._create_test_Applicant(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        for user_id in range(settings.USERS_PER_PAGE-1):
            self.assertContains(response, f'@user{user_id}')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'user{user_id}@test.org')
            user = User.objects.get(email=f'user{user_id}@test.org')
            user_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id': user.id})
            self.assertContains(response, user_url)

    def test_get_user_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_Member(self, user_count=10):
        for user_id in range(user_count):
            user = User.objects.create_user(f'@user{user_id}',
                email = f'user{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
                chess_Level = "1",
            )
            if user_id %2 == 0:
                Role.objects.create(club = self.club, user = user, club_role = 'Member')
            else:
                Role.objects.create(club = self.club, user = user, club_role = 'Officer')

    def _create_test_Applicant(self, user_count=10):
        for user_id in range(user_count):
            user = User.objects.create_user(f'@user{user_id}',
                email = f'user{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
                chess_Level = "1",
            )
            if user_id %2 == 0:
                Role.objects.create(club = self.club, user = user, club_role = 'Member')
            else:
                Role.objects.create(club = self.club, user = user, club_role = 'Applicant')
