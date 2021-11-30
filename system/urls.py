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
    path('log_in/', views.LogInView.as_view(), name ='log_in'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('change_password/<int:user_id>', views.change_password, name='change_password'),
    path('approve_member/<int:user_id>', views.approve_member, name ='approve_member'),
    path('promote/<int:user_id>', views.promote, name ='promote'),
    path('demote/<int:user_id>', views.demote, name ='demote'),
    path('transferownership/<int:user_id>/<int:request_user_id>', views.transferownership, name ='transferownership'),
    path('member_list/', views.member_list, name ='member_list')
]
