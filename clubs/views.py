from django.shortcuts import redirect, render
from .form import SignUpForm, LogInForm, UpdatePasswordForm, ProfileForm, ClubRegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import User, Club, Role
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden
from .helpers import *



def log_in(request):
    """View for logging in to the appp"""

    if request.method == 'POST' :
        form = LogInForm(request.POST)
        if form.is_valid():
            print('valid')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')

            messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm();
    return render(request, 'log_in.html', {'form':form, 'current_user':request.user})


def log_out(request):
    """View that logs out from the account"""

    logout(request)
    return redirect('home')


def home(request):
    return render(request,'home.html');


def sign_up(request):
    """View that signs up user."""

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('valid')
            user = form.save()
            messages.add_message(request, messages.SUCCESS, "Application successfully submitted")
            login(request, user)
            return redirect('clubs_list')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


@login_required
def list(request, club_id):
    """View for the list users registered to a club"""

    current_user = request.user
    clubs_in = current_user.get_clubs_in()
    current_club = Club.objects.get(id = club_id)
    current_role = current_club.get_club_role(current_user)
    if current_role== 'Applicant':
        users = current_club.get_Applicant()
    elif current_role== 'Owner' or current_role == 'Officer':
        users = current_club.get_all_Members()
    elif current_role== 'Member':
        users = current_club.get_Members()
    else:
        users = []
    return render(request,'list.html',{'users':users, 'current_role':current_role, 'current_club':current_club, 'clubs_in':clubs_in })


@login_required
def profile(request):
    """View for updating the profile for users"""
    current_user = request.user
    clubs_in = current_user.get_clubs_in()
    if request.method == 'POST':
        form = ProfileForm(instance = current_user, data = request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance = current_user)
    return render(request, 'profile.html', {'form':form,'clubs_in':clubs_in})


@login_required
def password(request):
    """View for update the password"""

    current_user = request.user
    if request.method == 'POST':
        form = UpdatePasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(request, messages.SUCCESS, "Password updated!")
                return redirect('profile')
    form = UpdatePasswordForm()
    return render(request, 'edit_password.html', {'form': form})


@login_required
def menu_show(request):
    current_user = request.user
    clubs_in = current_user.get_clubs_in()
    return render(request, 'menu.html', {'clubs_in',clubs_in})


@login_required
def show_user(request, club_id, user_id):
    """View for showing the details for every user"""

    try:
        current_club = Club.objects.get(id = club_id)
        select_user = User.objects.get(id = user_id)
        role = Role.objects.get(club = current_club, user = select_user)
        current_user = request.user
        current_role = current_club.get_club_role(current_user)
        if current_role == 'Officer' or current_role == 'Owner':
            show = True
        else:
            show = False
    except ObjectDoesNotExist:
        return redirect('clubs_list')
    else:
        return render(request, 'show_user.html', {'user': select_user, 'club':current_club, 'role':role, 'show':show, 'current_role':current_role})

@login_required
def promoteUser(request, role_id):
    """View for the owner to be able to promote a member to the officer status"""
    try:
        role = Role.objects.get(id = role_id)
        current_club = Club.objects.get(id = role.club.id)
        select_user = User.objects.get(id = role.user.id)
        current_user = request.user
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Club not exists")
        return redirect('list', club_id = current_club.id)
    else:

        if current_club.get_club_role(current_user) == 'Owner':
            if current_club.get_club_role(select_user) == 'Member':
                current_club.promote_for_club(select_user)
                messages.add_message(request, messages.SUCCESS, "Promote Successfully")
                return redirect('list', club_id = current_club.id)
            else:
                messages.add_message(request, messages.ERROR, "This user is already an officer, they cannot be promoted further")
                return redirect('list', club_id = current_club.id)
        else:
            messages.add_message(request, messages.ERROR, "You are not the owner of the club")
            return redirect('list', club_id = current_club.id)
        return redirect('list', club_id = current_club.id)

@login_required
def demoteUser(request, role_id):
    """View for the owner to be able to demote an officer to the member status"""

    try:
        role = Role.objects.get(id = role_id)
        current_club = Club.objects.get(id = role.club.id)
        select_user = User.objects.get(id = role.user.id)
        current_user = request.user
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Club not exists")
        return redirect('list', club_id = current_club.id)
    else:
        if current_club.get_club_role(current_user) == "Owner":
            if current_club.get_club_role(select_user) == 'Officer':
                current_club.demote_for_club(select_user)
                messages.add_message(request, messages.SUCCESS, "Demote Successfully")
                return redirect('list', club_id = current_club.id)
            else:
                messages.add_message(request, messages.ERROR, "This user is a member, they cannot be demoted further")
                return redirect('list', club_id = current_club.id)
        else:
            messages.add_message(request, messages.ERROR, "You are not the owner of the club")
            return redirect('list', club_id = current_club.id)
        return redirect('list', club_id = current_club.id)

@login_required
def acceptUser(request, role_id):
    """View for officers to accept applicants to a club"""

    try:
        role = Role.objects.get(id = role_id)
        current_club = Club.objects.get(id = role.club.id)
        select_user = User.objects.get(id = role.user.id)
        current_user = request.user
        current_role = Role.objects.get(user = current_user, club = current_club).club_role
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Club not exists")
        return redirect('list', club_id = current_club.id)
    else:
        if current_role == 'Officer' or current_role == 'Owner':
            if current_club.get_club_role(select_user)== 'Applicant':
                current_club.approve_for_club(select_user)
                messages.add_message(request, messages.SUCCESS, "Accept Successfully")
                return redirect('list', club_id = current_club.id)
            else:
                messages.add_message(request, messages.ERROR, "This user is already a member, they cannot be approve further")
                return redirect('list', club_id = current_club.id)
        else:
            messages.add_message(request, messages.ERROR, "You are not a officer or owner of this club")
            return redirect('list', club_id = current_club.id)
        return redirect('list', club_id = current_club.id)

@login_required
def deleteUser(request, role_id):
    try:
        role = Role.objects.get(id = role_id)
        current_club = Club.objects.get(id = role.club.id)
        select_user = User.objects.get(id = role.user.id)
        current_user = request.user
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Club not exists")
        return redirect('list', club_id = current_club.id)
    else:
        if current_role == 'Officer' or current_role == 'Owner':
            if current_club.get_club_role(select_user)== 'Applicant':
                current_club.delete_for_club(select_user)
                messages.add_message(request, messages.SUCCESS, "Delete Successfully")
                return redirect('list', club_id = current_club.id)
            else:
                messages.add_message(request, messages.ERROR, "This user is already a member, they cannot be deleted further")
                return redirect('list', club_id = current_club.id)
        else:
            messages.add_message(request, messages.ERROR, "You are not a officer or owner of this club")
            return redirect('list', club_id = current_club.id)
        return redirect('list', club_id = current_club.id)

@login_required
def applyUser(request, role_id):
    """View for users to apply to a club"""

    try:
        role = Role.objects.get(id = role_id)
        current_club = Club.objects.get(id = role.club.id)
        current_user = request.user
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Club not exists")
        return redirect('clubs_list')
    else:
        if current_club.get_club_role(current_user) == 'No role':
            current_club.apply_for_club(current_user)
            messages.add_message(request, messages.SUCCESS, "Apply Successfully")
            return redirect('clubs_list')
        else:
            messages.add_message(request, messages.ERROR, "You are already in the club")
            return redirect('clubs_list')

@login_required
def clubRegister(request):
    """View for a member of a club to register a new club"""

    if request.method == 'POST':
        current_user = request.user
        form = ClubRegisterForm(request.POST)
        if form.is_valid():
            print('valid')
            club = form.save()
            club.create_club(current_user)
            messages.add_message(request, messages.SUCCESS, "Application successfully submitted")
            return redirect('clubs_list')
    else:
        form = ClubRegisterForm()
    return render(request,'club_register.html',{'form':form})

@login_required
def clubs_home_page(request):
    """View for the page of all clubs"""

    clubs = Club.objects.all()
    user = request.user
    return render(request,'clubs_list.html',{'clubs':clubs, 'user':user} )


@login_required
def club_info(request, club_id):
    """View for listing the information for every club"""
    try:
        club = Club.objects.get(id = club_id)
        owner = Role.objects.get(club=club, club_role='Owner').user
        current_user = request.user
        club_role = club.get_club_role(current_user)
        role = Role.objects.get(club=club, user = current_user)
    except ObjectDoesNotExist:
        return redirect('clubs_list')
    else:
        return render(request, 'club_info.html', {'club': club, 'user':current_user, 'club_role':club_role, 'role':role, 'owner':owner})

@login_required
def transferOwner(request, role_id):
    """View for the owner to transfer the ownership to an officer"""

    try:
        role = Role.objects.get(id = role_id)
        current_club = Club.objects.get(id = role.club.id)
        select_user = User.objects.get(id = role.user.id)
        current_user = request.user
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "Club not exists")
        return redirect('clubs_list')
    else:

        if current_club.get_club_role(current_user) == "Owner":
            if current_club.get_club_role(select_user) == 'Officer':
                current_club.transfer_ownership(current_user, select_user)
                return redirect('list', club_id = current_club.id)
            else:
                messages.add_message(request, messages.ERROR, "This user is not an officer, they cannot become owner of the club without being an officer!")
                return redirect('list', club_id = current_club.id)
        else:
            messages.add_message(request, messages.ERROR, "You are not the owner of the club")
            return redirect('list', club_id = current_club.id)
