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
    path('', views.home, name = 'home'),
    path('sign_up/', views.sign_up, name ='sign_up'),
    path('log_in/', views.log_in, name ='log_in'),
    path('log_out/', views.log_out, name ='log_out'),
    path('profile/<int:club_id>/<int:user_id>', views.profile, name='profile'),
    path('edit_profile/<int:club_id>/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('change_password/<int:club_id>/<int:user_id>', views.change_password, name='change_password'),
    path('approve_member/<int:club_id>/<int:applicant_id>', views.approve_member, name ='approve_member'),
    path('promote_member_to_officer/<int:club_id>/<int:member_id>', views.promote_member_to_officer, name ='promote_member_to_officer'),
    path('demote_officer_to_member/<int:club_id>/<int:officer_id>', views.demote_officer_to_member, name ='demote_officer_to_member'),
    path('transfer_ownership/<int:club_id>/<int:new_owner_id>', views.transfer_ownership, name ='transfer_ownership'),
    path('member_list/<int:club_id>/', views.member_list, name ='member_list'),
    path('club_page/<int:club_id>/', views.club_page, name='club_page'),
    path('club_list/', views.club_list, name ='club_ist'),
    path('request_toggle/<int:user_id>/<int:club_id>', views.request_toggle, name = 'request_toggle'),
    ]
