"""Unit tests for the Role model."""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User, Club, Role

class RoleModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            chess_Level='3',
            bio='The quick brown fox jumps over the lazy dog.',
            personal_statement='this is John doe',
            is_staff=False,
            is_active=True,
            is_superuser=False
        )
        self.club = Club.objects.create(
            name = "Club 1",
            location = 'London',
            description = 'Chess club in London',
            number_of_members = 12
        )
        self.role = Role.objects.create(
            user = self.user,
            club = self.club,
            club_role = 'Applicant'
        )

    def assert_role_is_valid(self):
        try:
            self.role.full_clean()
        except (ValidationError):
            self.fail('Role should be valid')

    def assert_role_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.role.full_clean()

    def test_valid_role(self):
        self.assert_role_is_valid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_valid_user(self):
        self._assert_user_is_valid()

    def assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Club should be valid')

    def assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def test_valid_club(self):
        self.assert_club_is_valid()
