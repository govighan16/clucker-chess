from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Role
from clubs.tests.helpers import reverse_with_next

class UserListTest(TestCase):

    fixtures = [ 'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json'
                ]

    def setUp(self):
        self.club = Club.objects.get(pk = 1)
        self.user = User.objects.get(pk = 1)
        self.role = Role.objects.create(club=self.club, user = self.user, club_role = 'Applicant')
        self.url = reverse('clubs_list')


    def test_show_user_in_Officer_role_url(self):
        self.role = Role.objects.create(club=self.club, user = self.user, club_role = 'Officer')
        select_user = User.objects.get(pk = 2)
        self.url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        self.assertEqual(self.url,f'/user/{self.club.id}/{select_user.id}')

    def test_get_applicant_profile_for_Officer_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        select_user = User.objects.get(pk = 4)
        select_role = Role.objects.create(club=self.club, user = select_user, club_role = 'Applicant')
        select_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        response = self.client.get(select_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, '@davidsmith')
        self.assertContains(response, 'David')
        self.assertContains(response, 'Smith')
        self.assertContains(response, 'My bio')
        self.assertContains(response, "1")
        self.assertContains(response, 'davidsmith@example.org')
        self.assertContains(response, 'Hi I am David')
        self.assertContains(response, self.club.name)
        self.assertContains(response, 'Applicant')
        user = User.objects.get(email='davidsmith@example.org')
        role = Role.objects.get(club = self.club, user = user)
        accept_url = reverse('acceptUser', kwargs={'role_id':role.id})
        delete_url = reverse('deleteUser', kwargs={'role_id':role.id})
        #self.assertContains(response, accept_url)
        #self.assertContains(response, delete_url)


    def test_get_member_profile_for_Officer_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        select_user = User.objects.get(pk = 2)
        select_role = Role.objects.create(club=self.club, user = select_user, club_role = 'Member')
        select_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        response = self.client.get(select_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, '@janedoe')
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'Doe')
        self.assertContains(response, 'My bio')
        self.assertContains(response, "1")
        self.assertContains(response, 'janedoe@example.org')
        self.assertContains(response, self.club.name)
        self.assertContains(response, 'Member')

    def test_get_Officer_profile_for_Officer_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        select_user = User.objects.get(pk = 3)
        select_role = Role.objects.create(club=self.club, user = select_user, club_role = 'Officer')
        select_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        response = self.client.get(select_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, 'Maria')
        self.assertContains(response, 'Evans')
        self.assertContains(response, '@mariaevans')
        self.assertContains(response, 'My bio')
        self.assertContains(response, "1")
        self.assertContains(response, 'mariaevens@example.org')
        self.assertContains(response, 'Hi I am Maria')
        self.assertContains(response, self.club.name)
        self.assertContains(response, 'Officer')

    def test_show_user_in_Owner_role_url(self):
        self.role = Role.objects.create(club=self.club, user = self.user, club_role = 'Owner')
        select_user = User.objects.get(pk = 2)
        self.url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        self.assertEqual(self.url,f'/user/{self.club.id}/{select_user.id}')

    def test_get_applicant_profile_for_Owner_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        select_user = User.objects.get(pk = 4)
        select_role = Role.objects.create(club=self.club, user = select_user, club_role = 'Applicant')
        select_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        response = self.client.get(select_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, '@davidsmith')
        self.assertContains(response, 'David')
        self.assertContains(response, 'Smith')
        self.assertContains(response, 'My bio')
        self.assertContains(response, "1")
        self.assertContains(response, 'davidsmith@example.org')
        self.assertContains(response, 'Hi I am David')
        self.assertContains(response, self.club.name)
        self.assertContains(response, 'Applicant')
        user = User.objects.get(email='davidsmith@example.org')
        role = Role.objects.get(club = self.club, user = user)
        accept_url = reverse('acceptUser', kwargs={'role_id':role.id})
        delete_url = reverse('deleteUser', kwargs={'role_id':role.id})
        #self.assertContains(response, accept_url)
        #self.assertContains(response, delete_url)

    def test_get_member_profile_for_Owner_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        select_user = User.objects.get(pk = 2)
        select_role = Role.objects.create(club=self.club, user = select_user, club_role = 'Member')
        select_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        response = self.client.get(select_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, '@janedoe')
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'Doe')
        self.assertContains(response, 'My bio')
        self.assertContains(response, "1")
        self.assertContains(response, 'janedoe@example.org')
        self.assertContains(response, self.club.name)
        self.assertContains(response, 'Member')
        user = User.objects.get(email='janedoe@example.org')
        role = Role.objects.get(club = self.club, user = user)
        promote_url = reverse('promoteUser', kwargs={'role_id':role.id})
        #self.assertContains(response, promote_url)


    def test_get_Officer_profile_for_Owner_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        select_user = User.objects.get(pk = 3)
        select_role = Role.objects.create(club=self.club, user = select_user, club_role = 'Officer')
        select_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        response = self.client.get(select_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, 'Maria')
        self.assertContains(response, 'Evans')
        self.assertContains(response, '@mariaevans')
        self.assertContains(response, 'My bio')
        self.assertContains(response, "1")
        self.assertContains(response, 'mariaevens@example.org')
        self.assertContains(response, 'Hi I am Maria')
        self.assertContains(response, self.club.name)
        self.assertContains(response, 'Officer')
        user = User.objects.get(email='mariaevens@example.org')
        role = Role.objects.get(club = self.club, user = user)
        demote_url = reverse('demoteUser', kwargs={'role_id':role.id})
        transfer_url = reverse('transferOwnership', kwargs={'role_id':role.id})
        #self.assertContains(response, demote_url)
        #self.assertContains(response, transfer_url)

    def test_show_user_url_in_Member_role_url(self):
        self.role = Role.objects.create(club=self.club, user = self.user, club_role = 'Member')
        select_user = User.objects.get(pk = 2)
        self.url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        self.assertEqual(self.url,f'/user/{self.club.id}/{select_user.id}')


    def test_get_member_profile_for_Member_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        select_user = User.objects.get(pk = 2)
        select_role = Role.objects.create(club=self.club, user = select_user, club_role = 'Member')
        select_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        response = self.client.get(select_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, '@janedoe')
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'Doe')
        self.assertContains(response, 'My bio')
        self.assertContains(response, "1")
        self.assertContains(response, 'janedoe@example.org')
        self.assertContains(response, self.club.name)
        self.assertContains(response, 'Member')


    def test_show_user_in_Applicant_role_url(self):
        self.role = Role.objects.create(club=self.club, user = self.user, club_role = 'Applicant')
        select_user = User.objects.get(pk = 2)
        self.url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        self.assertEqual(self.url,f'/user/{self.club.id}/{select_user.id}')

    def test_get_applicant_profile_for_Applicant_Role(self):
        self.client.login(email=self.user.email, password='Password123')
        select_user = User.objects.get(pk = 4)
        select_role = Role.objects.create(club=self.club, user = select_user, club_role = 'Applicant')
        select_url = reverse('show_user', kwargs={'club_id':self.club.id, 'user_id':select_user.id})
        response = self.client.get(select_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, '@davidsmith')
        self.assertContains(response, 'David')
        self.assertContains(response, 'Smith')
        self.assertContains(response, 'My bio')
        self.assertContains(response, "1")
        self.assertContains(response, 'davidsmith@example.org')
        self.assertContains(response, 'Hi I am David')
        self.assertContains(response, self.club.name)
        self.assertContains(response, 'Applicant')
