"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('log_in/', views.log_in, name = 'log_in'),
    path('user/<int:club_id>/<int:user_id>', views.show_user, name='show_user'),
    path('list/<int:club_id>', views.list, name='list'),
    path('club/<int:club_id>', views.club_info, name='club_info'),
    path('log_out/', views.log_out, name = 'log_out'),
    path('edit_password/', views.password, name='edit_password'),
    path('profile/', views.profile, name = 'profile'),
    path('promote/<int:role_id>', views.promoteUser, name='promoteUser'),
    path('demote/<int:role_id>', views.demoteUser, name='demoteUser'),
    path('accept/<int:role_id>', views.acceptUser, name='acceptUser'),
    path('delete/<int:role_id>', views.deleteUser, name='deleteUser'),
    path('transfer/<int:role_id>', views.transferOwner, name='transferOwnership'),
    path('apply/<int:role_id>', views.applyUser, name='applyUser'),
    path('club_register/', views.clubRegister, name='club_register'),
    path('clubs_list/', views.clubs_home_page, name='clubs_list'),
    path('transfer/<int:user_id>', views.transferOwner, name='transferOwner'),

]
