from .views import *
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views


# urlpatterns = [
#     path('login', LoginView.as_view(), name="login"),
#     path('register', RegistrationView.as_view(), name="register"),

#     path('logout', LogoutView.as_view(), name="logout"),
#     path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
#     path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
#     path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),


#     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


# ]

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "validate-username/", UsernameValidationView.as_view(), name="validate-username"
    ),
    path("validate-email/", EmailValidationView.as_view(), name="validate_email"),
    path("activate/<uidb64>/<token>/", VerificationView.as_view(), name="activate"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="authentication/password_reset_form.html",
            email_template_name="authentication/password_reset_email.html",
           
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="authentication/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authentication/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
