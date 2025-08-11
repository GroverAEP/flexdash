from django.contrib import admin
from django.urls import path
from frontend import views

urlpatterns = [
    ##forntend para administrador - super usuario o propietario agregan la cuenta del admin
    path("account/login",views.accountLogin, name="login"),
    # path("account/register",views.accountRegister, name="register"),

    path("account/auth",views.accountAuth, name="auth"),


    # dahsboard for account
    path("account/dashboard",views.accountDashboard, name="account-dashboard"),
    path("account/business",views.accountBusiness, name="account-business"),
    
    #dashboard for business
    path("business/dashboard",views.accountBusinessDashboard, name="account-business-dashboard"),
    path("business/preorders",views.accountBusinessPreorders, name="account-business-preorders"),
    
    #options for business
    path("business/options/", views.options, name="options"),

    #options general
    path("options/password_reset",views.optionPassword_reset, name="password_reset"),
    path("options/logout",views.optionLogout, name="logout")
]

