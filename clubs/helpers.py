from django.shortcuts import redirect, render
from .models import User, Club, Role
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_function(request)
    return modified_view_function


def member_required(view_function):
    def modified_view_function(request,club_name,args,*kwargs):
      try:
          club = Club.objects.get(club_name=club_name)
          role = request.user.role_set.get(club=club)
      except ObjectDoesNotExist:
          return redirect('home')
      else:
          if role.club_role == 'MEMBER':
             return view_function(request,club_name,args,*kwargs)
          else:
            return redirect(view_function(request))
    return modified_view_function


def owner_required(view_function):
    def modified_view_function(request,club_name,args,*kwargs):
        try:
            club = Club.objects.get(club_name=club_name)
            role = request.user.role_set.get(club=club)
        except ObjectDoesNotExist:
            return redirect('home')
        else:
            if role.club_role == 'OWNER':
                return view_function(request,club_name,args,*kwargs)
            else:
                return redirect(view_function(request))
    return modified_view_function

def membership_required(view_function):
    def modified_view_function(request,club_name,args,*kwargs):
        try:
            club = Club.objects.get(club_name=club_name)
            role = request.user.role_set.get(club=club)
        except ObjectDoesNotExist:
            return redirect('home')
        else:
            if role.club_role == 'MEMEMBER' or role.club_role == 'OFFICER' or role.club_role == 'OWNER':
                return view_function(request,club_name,args,*kwargs)
            else:
                return redirect(view_function(request))
    return modified_view_function


def club_exists(view_function):
    def modified_view_function(request,club_name,args,*kwargs):
        try:
            club = Club.objects.get(club_name=club_name)
        except ObjectDoesNotExist:
            return redirect('home')
        else:
            return view_function(request,club_name,args,*kwargs)
    return modified_view_function
