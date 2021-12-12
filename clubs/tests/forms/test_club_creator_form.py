from django import forms
from django.test import TestCase
from clubs.forms import ClubCreatorForm
from clubs.models import User, Club


class ClubCreatorTestCase(TestCase):
    """Unit tests for the Club Creator Form."""


    def setUp(self):
        self.form_input = {
            'name': 'Club A',
            'city': 'London',
            'description': 'This is the description'
        }

    def test_valid_club_creator_form(self):
        form = ClubCreatorForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = ClubCreatorForm()
        self.assertIn('name', form.fields)
        self.assertIn('city', form.fields)
        self.assertIn('description', form.fields)
        self.assertNotIn('location', form.fields)
        self.assertNotIn('users', form.fields)
    
    def test_form_rejects_blank_name(self):
        self.form_input['name']= ''
        form = ClubCreatorForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_city(self):
        self.form_input['city']= ''
        form = ClubCreatorForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_description(self):
        self.form_input['description']= ''
        form = ClubCreatorForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save_correctly(self):
        form = ClubCreatorForm(data=self.form_input)
        before_count = Club.objects.count()
        form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        club = Club.objects.get(name='Club A')
        self.assertEqual(club.name, 'Club A')
        self.assertEqual(club.city, 'London')
        self.assertEqual(club.description, 'This is the description')

