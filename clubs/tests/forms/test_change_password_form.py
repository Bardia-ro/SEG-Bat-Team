from django import forms
from django.test import TestCase
from clubs.forms import ChangePasswordForm
from clubs.models import User

class ChangePasswordFormTestCase(TestCase):
    """Unit tests for the Sign Up Form."""

    def setUp(self):
        self.form_input = {
            'new_password': 'NewPassword123',
            'password_confirmation': 'NewPassword123'
        }

    #Form accepts valid input data
    def test_valid_sign_up_form(self):
        form = ChangePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = ChangePasswordForm()
        self.assertIn('new_password', form.fields)
        self.assertIn('password_confirmation', form.fields)
    
    def test_form_rejects_blank_password(self):
        self.form_input['new_password']= ''
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_passowrd_confirmation(self):
        self.form_input['password_confirmation']= ''
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = ChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    