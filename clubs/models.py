"""Models in the chess clubs app."""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from libgravatar import Gravatar
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class MyUserManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, bio, personal_statement, chess_Level):
        email = self.normalize_email(email)
        user = self.model(
                first_name = first_name,
                last_name = last_name,
                email = email,
                bio = bio,
                personal_statement = personal_statement,
                chess_Level = chess_Level

        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, first_name, last_name, username, email, bio, personal_statement, chess_Level):
        user = self.create_user(first_name, last_name, username, email, bio, personal_statement, chess_Level)
        user.save(using=self._db)
        return user


    def create_club(self, name, location, description, number_of_members):
        club = self.model(
                name = name,
                location = location,
                description = description,
                number_of_members = number_of_members
                )
        club.save(using=self._db)
        return club




# Create your models here.
class User(AbstractUser):
    """User model used for authentication and using the chess club app."""

    username = models.CharField(
        max_length=30,
        unique= True,
        blank = False,
        validators=[RegexValidator(
            regex= r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals.'
        )]
    )

    first_name = models.CharField( max_length=50, unique= False, blank=False )

    last_name = models.CharField( max_length=50, unique= False, blank=False)

    email = models.EmailField(unique = True, blank = False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    bio = models.TextField(blank=True)

    personal_statement = models.TextField(blank=True)

    #Users can select their chess level from a choice box containg 5 different levels.
    level_Choice = (("1", "One"),
                ("2", "Two"),
                ("3", "Three"),
                ("4", "Four"),
                ("5", "Five"),)

    chess_Level = models.CharField(max_length=30, choices=level_Choice)

    def get_clubs_in(self):
        clubs = Club.objects.all()
        current_user=self
        return Club.objects.all().filter(
        club_members__username = current_user.username
        ).exclude( Q(role__club_role = 'Applicant') | Q(role__club_role = 'No role') )


    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url




class Club(models.Model):
    """Club model used to register a new club in the app."""

    name = models.CharField( max_length = 100, unique = True, blank = False)
    location = models.CharField( max_length = 100, unique = False, blank = False)
    description = models.TextField( max_length = 300, blank = False)
    number_of_members = models.IntegerField(default=1)


    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    club_members = models.ManyToManyField(User,through='Role')

    def get_club_role(self,user):
        """Return the role of an user in clubs"""

        try:
            role = Role.objects.get(club=self, user=user)
        except ObjectDoesNotExist:
            role = Role.objects.create(club=self,
                                       user=user)
            role.club_role = 'No role'
            role.save()
            return role.club_role
        else:
            return role.club_role

    def create_club(self,user):
        """Creates a new club.
            The user that registers a new club will automatically be the owner of the new club"""

        role = Role.objects.create(club=self,
                                   user=user)
        role.club_role = 'Owner'
        role.save()

    def apply_for_club(self,user):
        """Users of the app can apply for membership to any clubs"""

        role = Role.objects.get(club=self,user=user)
        role.club_role = 'Applicant'
        self.number_of_members += 1
        self.save()
        role.save()

    def approve_for_club(self,user):
        """The application for a club is approved by an officer so the applicant becomes a member"""

        role = Role.objects.get(club=self,user=user)
        if role.club_role == 'Applicant':
            role.club_role = 'Member'
            role.save()
            return
        else:
            return

    def delete_for_club(self,user):
        """The application for a club is denied by an officer"""

        role = Role.objects.get(club=self,user=user)
        if role.club_role == 'Applicant':
            role.delete()
            self.number_of_members -= 1
            self.save()
            return
        else:
            return

    def demote_for_club(self,user):
        """An officer is demoted and becomes an usual member of the club"""

        role = Role.objects.get(club=self,user=user)
        if role.club_role == 'Officer':
            role.club_role = 'Member'
            role.save()
            return
        else:
            return

    def promote_for_club(self,user):
        """A member is promoted to the officer status"""

        role = Role.objects.get(club=self,user=user)
        if role.club_role == 'Member':
            role.club_role = 'Officer'
            role.save()
            return
        else:
            return

    def remove_for_club(self,user):
        """Memebers can be removed from clubs"""

        role = Role.objects.get(club=self, user=user)
        if role.club_role == "Member":
            role.club_role = 'No role'
            self.number_of_members -= 1
            self.save()
            role.save()
            return
        else:
            return

    def transfer_ownership(self, owner, officer):
        """The owner transfers the ownership to an officer"""

        owner_role = Role.objects.get(club=self, user=owner)
        officer_role = Role.objects.get(club=self, user=officer)
        if owner_role.club_role == 'Owner':
            if officer_role.club_role == 'Officer':
                officer_role.club_role = 'Owner'
                owner_role.club_role = 'Officer'
                officer_role.save()
                owner_role.save()
                return
            else:
                messages.add_message(request, messages.ERROR, "You can't transfer to someone who are not the officer")
        else:
            messages.add_message(request, messages.ERROR, "You are not the owner of this club")
            return

    def get_Applicant(self):
        """Returns all applicants for a club"""

        return User.objects.all().filter(
            club__name = self.name,
            role__club_role = 'Applicant'
        )

    def get_Members(self):
        """Returns all members in a club"""

        return User.objects.all().filter(
            club__name = self.name
        ).exclude ( Q(role__club_role = 'Applicant') | Q(role__club_role = 'No role') )

    def get_all_Members(self):
        """Returns all applicants and members in a club"""
        return User.objects.all().filter(
            club__name = self.name
        ).exclude(role__club_role = 'No role')



class Role(models.Model):
    """Roles an user can have in a club"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    club_role = models.CharField(
        max_length = 100,
        default = "Applicant"
        )
