from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from .models import User

#options for the 'experience' drop down box
EXPERIENCE_CHOICES = [
('class D', 'Class D'),
('class C', 'Class C'),
('class B', 'Class B'),
('class A', 'Class A'),
('expert', 'Expert'),
('master', 'Master'),
]

class Password():
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio','experience','personal_statement']
        widgets = { 'bio': forms.Textarea(), 'personal_statement': forms.Textarea(),'experience': forms.Select(choices = EXPERIENCE_CHOICES)}

    new_password = Password.new_password
    password_confirmation = Password.password_confirmation

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        """Create a new user."""
        super().save(commit=False)
        user = User.objects.create_user(
            username= self.cleaned_data.get('email'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            bio=self.cleaned_data.get('bio'),
            password=self.cleaned_data.get('new_password'),
            experience = self.cleaned_data.get('experience'),
            personal_statement = self.cleaned_data.get('personal_statement')
        )
        return user

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio','experience','personal_statement']
        widgets = { 'bio': forms.Textarea(), 'personal_statement': forms.Textarea(),'experience': forms.Select(choices = EXPERIENCE_CHOICES)}

class ChangePasswordForm(forms.ModelForm, Password):
    class Meta:
        model = User
        fields = []

    new_password = Password.new_password
    password_confirmation = Password.password_confirmation

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        self.instance.set_password(self.cleaned_data.get('new_password'))
        self.instance.save()
        user = authenticate(username=self.instance.username, password=self.cleaned_data.get('new_password'))
        return user