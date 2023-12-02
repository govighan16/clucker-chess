"""Unit tests of the club register form."""
from django import forms
from django.test import TestCase
from clubs.form import ClubRegisterForm
from clubs.models import Club

class ClubRegisterFormTestCase(TestCase):
    """Unit tests of the club registration form."""

    def setUp(self):
        self.form_input = {
            'name': 'Club 1',
            'location': 'London',
            'description': 'The London Chess Club',
        }

    def test_valid_sign_up_form(self):
        form = ClubRegisterForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_contains_required_fields(self):
        form = ClubRegisterForm()
        self.assertIn('name', form.fields)
        self.assertIn('location', form.fields)
        self.assertIn('description', form.fields)

    def test_form_accepts_valid_input(self):
        form = ClubRegisterForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_name(self):
        self.form_input['name'] = ''
        form = ClubRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_location(self):
        self.form_input['location'] = ''
        form = ClubRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_description(self):
        self.form_input['description'] = ''
        form = ClubRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = ClubRegisterForm(data=self.form_input)
        before_count = Club.objects.count()
        form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        club = Club.objects.get(name='Club 1')
        self.assertEqual(club.location, 'London')
        self.assertEqual(club.description, 'The London Chess Club')
