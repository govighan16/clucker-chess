"""Unit tests for the Club model."""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User, Club

class ClubModelTestCase(TestCase):

    def setUp(self):
        self.club = Club.objects.create(name = "Club 1", location = 'London', description = 'Chess club in London', number_of_members = 12)
        self.club2= Club.objects.create(name = "Club 2", location = 'New York', description = 'Chess club in New York', number_of_members = 20)

    def assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Club should be valid')

    def test_valid_club(self):
        self.assert_club_is_valid()

    def assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def test_club_name_is_unique(self):
        self.club.name = self.club2.name
        self.assert_club_is_invalid()

    def test_name_cannot_be_over_100_characters_long(self):
        self.club.name = 'x' * 101
        self.assert_club_is_invalid()

    def test_name_can_be_100_characters_long(self):
        self.club.name = 'x' * 99
        self.assert_club_is_valid()

    def test_location_cannot_be_over_100_characters_long(self):
        self.club.location = 'x' * 101
        self.assert_club_is_invalid()

    def test_location_can_be_100_characters_long(self):
        self.club.location = 'x' * 100
        self.assert_club_is_valid()

    def test_description_cannot_be_over_300_characters_long(self):
        self.club.name = 'x' * 301
        self.assert_club_is_invalid()

    def test_description_can_be_300_characters_long(self):
        self.club.description = 'x' * 300
        self.assert_club_is_valid()

    def test_club_name_must_not_be_blank(self):
        self.club.name = ''
        self.assert_club_is_invalid()

    def test_club_location_must_not_be_blank(self):
        self.club.location = ''
        self.assert_club_is_invalid()

    def test_club_description_must_not_be_blank(self):
        self.club.description = ''
        self.assert_club_is_invalid()
