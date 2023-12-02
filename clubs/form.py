
"""Forms for the chess clubs app."""
from .models import User, Club
from django.core.validators import RegexValidator
from django import forms


class SignUpForm(forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'chess_Level', 'personal_statement']


        widgets = {'bio': forms.Textarea(),
                   'personal_statement': forms.Textarea(),
                   }


    new_password =  forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(),
        validators = [RegexValidator(
            regex= r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message= 'Password must contain an uppercase character, a lowercase '
                      'character and a number'
            )
            ]
    )

    password_confirmation = forms.CharField(label='Password Confirmation', widget = forms.PasswordInput())


    level_Choice = (
                    ("1", "One"),
                    ("2", "Two"),
                    ("3", "Three"),
                    ("4", "Four"),
                    ("5", "Five"),
                  )


    chess_Level = forms.ChoiceField(choices = level_Choice)

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password')

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
            bio = self.cleaned_data.get('bio'),
            chess_Level = self.cleaned_data.get('chess_Level'),
            personal_statement = self.cleaned_data.get('personal_statement'),
        )
        return user



class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())



class ProfileForm(forms.ModelForm):
    """Form to update user profiles"""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'chess_Level', 'personal_statement']

        widgets = {'bio': forms.Textarea(),
                   'personal_statement': forms.Textarea(),
                   }

        level_Choice = (
                        ("1", "One"),
                        ("2", "Two"),
                        ("3", "Three"),
                        ("4", "Four"),
                        ("5", "Five"),
                      )
        chess_Level = forms.ChoiceField(choices = level_Choice)


class UpdatePasswordForm(forms.Form):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())
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

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class ClubRegisterForm(forms.ModelForm):
    """ Form enabling registered users to create a club"""

    class Meta:
        """Form options."""

        model = Club
        fields = [ 'name', 'location', 'description']
        widgets = {'description': forms.Textarea()}

    def save(self):
        """Create a new club."""

        super().save(commit=False)
        club = Club.objects.create(
            name=self.cleaned_data.get('name'),
            location=self.cleaned_data.get('location'),
            description=self.cleaned_data.get('description'),
            number_of_members=1
        )
        return club
