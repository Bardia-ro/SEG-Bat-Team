"""Unit test for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User


class UserModelTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json']

    """Unit tests for the User model."""
    def setUp(self):
        self.user=User.objects.get(email='johndoe@example.org')

    def test_valid_user(self):
        self.assert_user_is_valid()

    def test_first_name_must_not_be_blank(self):
        self.user.first_name=''
        self.assert_user_is_invalid()

    def test_first_name_need_not_to_be_unique(self):
        second_user = User.objects.get(email='janedoe@example.org')
        self.user.first_name = second_user.first_name
        self.assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self.assert_user_is_valid()

    def test_first_name_may_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self.assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self.assert_user_is_invalid()

    def test_last_name_need_not_to_be_unique(self):
        second_user = User.objects.get(email='janedoe@example.org')
        self.user.last_name = second_user.last_name
        self.assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self.assert_user_is_valid()

    def test_last_name_may_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self.assert_user_is_invalid()

    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self.assert_user_is_invalid()

    def email_need_must_be_unique(self):
        second_user = User.objects.get(username='janedoe@example.org')
        self.user.email = second_user.email
        self.assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self.assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self.assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@org'
        self.assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self.assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self.assert_user_is_invalid()


    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self.assert_user_is_valid()

    def bio_may_contain_520_characters(self):
        self.user.bio = 'x' * 520
        self.assert_user_is_valid()

    def bio_may_not_contain_more_than_520_characters(self):
        self.user.bio = 'x' * 521
        self.assert_user_is_invalid()

    def bio_need_not_to_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.bio = second_user.bio
        self.assert_user_is_valid()

    def experience_cannot_be_blank(self):
        self.user.experience = ''
        self.assert_user_is_valid()
    
    def experience_must_be_one_of_options_given(self):
        self.user.experience = 'class Z'
        self.assert_user_is_valid()



    def test_personal_statement_must_not_be_blank(self):
        self.user.personal_statement = ''
        self.assert_user_is_invalid()

    def bio_may_contain_600_characters(self):
        self.user.personal_statement = 'x' * 520
        self.assert_user_is_valid()

    def bio_may_not_contain_more_than_600_characters(self):
        self.user.bio = 'x' * 601
        self.assert_user_is_invalid()

    def bio_need_not_to_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.bio = second_user.bio
        self.assert_user_is_valid()


    def assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()