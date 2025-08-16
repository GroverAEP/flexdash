
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
# from django.contrib.auth import User

from django.http import HttpResponse

class AuthContent():
    @classmethod
    def vef_auth_session(self, user):
        if user.is_authenticated:
                return redirect("account-dashboard")

    @classmethod
    def reg_user_admin(self,user):
        # user = user.object.create_user()
        pass