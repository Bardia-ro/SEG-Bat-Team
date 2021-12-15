from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Role

class RoleModelTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user=User.objects.get(email='johndoe@example.org')
        self.club=Club.objects.get(name='Club A')
        self.role=Role.objects.get(club=self.club, user__id=self.user.id)

    def test_valid_role(self):
        self.assert_role_is_valid()

    def test_user_must_not_be_blank(self):
        self.role.user = None
        self.assert_role_is_invalid()

    def test_club_must_not_be_blank(self):
        self.role.club = None
        self.assert_role_is_invalid()

    def test_role_must_not_be_blank(self):
        self.role.role=None
        self.assert_role_is_invalid()

    def test_role_must_valid_choice(self):
        self.role.role=5
        self.assert_role_is_invalid()

    def test_assert_owner_role_assigned_correctly(self):
        self.role.role = 4
        role_name = self.role.role_name()
        self.assertAlmostEqual("Owner" ,role_name)

    def test_assert_officer_role_assigned_correctly(self):
        self.role.role = 3
        role_name = self.role.role_name()
        self.assertAlmostEqual("Officer" ,role_name)

    def test_assert_member_role_assigned_correctly(self):
        self.role.role = 2
        role_name = self.role.role_name()
        self.assertAlmostEqual("Member" ,role_name)
    
    def test_assert_applicant_role_assigned_correctly(self):
        self.role.role = 1
        role_name = self.role.role_name()
        self.assertAlmostEqual("Applicant" ,role_name)
    
    def test_elo_rating_must_not_be_blank(self):
        self.role.elo_rating = ''
        self.assert_role_is_invalid()
    
    def test_elo_rating_sets_default(self):
        self.assertEqual(self.role.elo_rating,1000)

    
    def assert_role_is_valid(self):
        try:
            self.role.full_clean()
        except (ValidationError):
            self.fail('Club should be valid')

    def assert_role_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.role.full_clean()