from django import forms
from django.test import TestCase
from clubs.forms import TournamentForm
from clubs.models import Tournaments, User, Club


class TournamentCreatorTestCase(TestCase):
    """Unit tests for the Sign Up Form."""

    fixtures = [
        "clubs/tests/fixtures/default_user.json",
        "clubs/tests/fixtures/default_club.json"]

    def setUp(self):
        self.user =User.objects.get(email="johndoe@example.org")
        self.club =Club.objects.get(name ="Club A")
        self.form_input = {
            'name': 'Tournament A',
            'description': 'This is the description',
            'capacity': 4,
            'deadline': "2021-01-12 14:12:06"
        }

    def test_valid_club_creator_form(self):
        form = TournamentForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = TournamentForm()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('capacity', form.fields)
        self.assertIn('deadline', form.fields)
        deadline_field = form.fields['deadline']
        self.assertTrue(isinstance(deadline_field, forms.DateTimeField))
        self.assertNotIn('club', form.fields)
        self.assertNotIn('organiser', form.fields)
        self.assertNotIn('contender', form.fields)
    
    def test_form_rejects_blank_name(self):
        self.form_input['name']= ''
        form = TournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_description_city(self):
        self.form_input['description']= ''
        form = TournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_capacity(self):
        self.form_input['capacity']= ''
        form = TournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_deadline(self):
        self.form_input['deadline']= ''
        form = TournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save_correctly(self):
        form = TournamentForm(data=self.form_input)
        before_count = Tournaments.objects.count()
        form.save(self.user, self.club)
        after_count = Tournaments.objects.count()
        self.assertEqual(after_count, before_count+1)
        tournament = Tournaments.objects.get(name='Tournament A')
        self.assertEqual(tournament.name, 'Tournament A')
        self.assertEqual(tournament.description, 'This is the description')
        self.assertEqual(tournament.capacity, 4)
        #self.assertEqual(tournament.deadline, '2021-01-12 14:12:06')
