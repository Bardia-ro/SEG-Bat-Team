from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from clubs.forms import EditProfileForm
from clubs.models import User

class EditProfileFormTestCase(TestCase):
    """Unit tests for the EditProfile Form."""

    fixtures = ["clubs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.form_input = {
            'first_name': 'Jonathan',
            'last_name': 'Doetwo',
            'bio': 'My bio',
            'experience' : 'class D',
            'personal_statement' : 'My statement'
        }

    #Form accepts valid input data
    def test_valid_edit_profile_form(self):
        form = EditProfileForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = EditProfileForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('bio', form.fields)
        bio_widget = form.fields['bio'].widget
        self.assertTrue(isinstance(bio_widget, forms.Textarea))
        self.assertIn('experience', form.fields)
        type_field_widget = form.fields['experience'].widget
        self.assertTrue(isinstance(type_field_widget, forms.Select))
        self.assertIn('personal_statement', form.fields)
        personal_statement_widget = form.fields['personal_statement'].widget
        self.assertTrue(isinstance(personal_statement_widget, forms.Textarea))
    
    def test_form_rejects_blank_first_name(self):
        self.form_input['first_name']= ''
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_last_name(self):
        self.form_input['last_name']= ''
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_personal_statement(self):
        self.form_input['personal_statement']= ''
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    

    def test_form_must_save_correctly(self):
        user = User.objects.get(email='johndoe@example.org')
        form = EditProfileForm(data=self.form_input, instance=user)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.bio, 'Hey guys!')
        self.assertEqual(user.experience, 'class D')
        self.assertEqual(user.personal_statement, 'Hi everyone. I love chess!')
        form.save()
        self.assertEqual(user.first_name, 'Jonathan')
        self.assertEqual(user.last_name, 'Doetwo')
        self.assertEqual(user.bio, 'My bio')
        self.assertEqual(user.experience, 'class D')
        self.assertEqual(user.personal_statement, 'My statement')
