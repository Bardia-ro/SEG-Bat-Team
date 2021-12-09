from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from clubs.forms import ChangePasswordForm
from clubs.models import User

class ChangePasswordFormTestCase(TestCase):
    """Unit tests for the ChangePassword Form."""

    fixtures = ["clubs/tests/fixtures/default_user.json"]

    def setUp(self):
        self.form_input = {
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    #Form accepts valid input data
    def test_valid_sign_up_form(self):
        form = ChangePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = ChangePasswordForm()
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password']= 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password']= 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password']= 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_must_be_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form_input = {
            'new_password': 'NewPassword456',
            'password_confirmation': 'NewPassword456'
        }
        user = User.objects.get(id=200)
        form = ChangePasswordForm(data=form_input, instance=user)
        self.assertTrue(form.is_valid())
        self.assertTrue(check_password('Password123', user.password))
        form.save()
        self.assertTrue(check_password('NewPassword456', user.password))