from django import forms
from django.test import TestCase
from clubs.forms import EditProfileForm
from clubs.models import User

class EditProfileFormTestCase(TestCase):
    """Unit tests for the Sign Up Form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'bio': 'New bio',
            'experience' : 'Class D',
            'personal_statement' : 'New statement'
        }

    #Form accepts valid input data
    def test_valid_sign_up_form(self):
        form = EditProfileForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = EditProfileForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('bio', form.fields)
        self.assertIn('personal_statement', form.fields)
        self.assertIn('experience', form.fields)
        type_field_widget = form.fields['experience'].widget
        self.assertTrue(isinstance(type_field_widget, forms.Select))
    
    def test_form_rejects_blank_first_name(self):
        self.form_input['first_name']= ''
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_last_name(self):
        self.form_input['last_name']= ''
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_bio(self):
        self.form_input['bio']= ''
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_personal_statement(self):
        self.form_input['personal']= ''
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save_correctly(self):
        form = EditProfileForm(data=self.form_input)
        before = User.objects.get(email='johndoe@example.org')
        form.save()
        after = User.objects.get(email='johndoe@example.org')
        self.assertNotEqual(after, before)
        self.assertEqual(after.first_name, 'Jane')
        self.assertEqual(after.last_name, 'Doe')
        self.assertEqual(after.email, 'johndoe@example.org')
        self.assertEqual(after.bio, 'New bio')
        self.assertEqual(after.personal_statement, 'New statement')
        self.assertEqual(after.experience, 'Class D')
