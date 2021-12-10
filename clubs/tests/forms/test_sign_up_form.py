from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from clubs.forms import SignUpForm
from clubs.models import User

class SignUpFormTestCase(TestCase):
    """Unit tests for the Sign Up Form."""

    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.com',
            'bio': 'My bio',
            'experience' : 'Class D',
            'personal_statement' : 'My statement',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    #Form accepts valid input data
    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)
        bio_widget = form.fields['bio'].widget
        self.assertTrue(isinstance(bio_widget, forms.Textarea))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))
        self.assertIn('experience', form.fields)
        type_field_widget = form.fields['experience'].widget
        self.assertTrue(isinstance(type_field_widget, forms.Select))
        self.assertIn('personal_statement', form.fields)
        personal_statement_widget = form.fields['personal_statement'].widget
        self.assertTrue(isinstance(personal_statement_widget, forms.Textarea))
        

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password']= 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password']= 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password']= 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confrimtaino_are_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = SignUpForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        user = User.objects.get(email='janedoe@example.com')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.com')
        self.assertEqual(user.bio, 'My bio')
        self.assertEqual(user.personal_statement, 'My statement')
        self.assertEqual(user.experience, 'Class D')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        