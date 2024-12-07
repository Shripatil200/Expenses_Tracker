
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from validate_email import validate_email
from django.urls import reverse
from userpreferences.models import UserPreference
from django.http import JsonResponse
import json
from django.contrib import auth
from .utils import account_activation_token





# Create your views here.


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})


# class RegistrationView(View):
#     def get(self, request):
#         return render(request, 'authentication/register.html')

#     def post(self, request):
#         # GET USER DATA
#         # VALIDATE
#         # create a user account

#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         context = {
#             'fieldValues': request.POST
#         }

#         if not User.objects.filter(username=username).exists():
#             if not User.objects.filter(email=email).exists():
#                 if len(password) < 6:
#                     messages.error(request, 'Password too short')
#                     return render(request, 'authentication/register.html', context)

#                 user = User.objects.create_user(username=username, email=email)
#                 user.set_password(password)
#                 user.is_active = False
#                 user.save()
#                 current_site = get_current_site(request)
#                 email_body = {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': account_activation_token.make_token(user),
#                 }

#                 link = reverse('activate', kwargs={
#                                'uidb64': email_body['uid'], 'token': email_body['token']})

#                 email_subject = 'Activate your account'

#                 activate_url = 'http://'+current_site.domain+link

#                 email = EmailMessage(
#                     email_subject,
#                     'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
#                     'noreply@semycolon.com',
#                     [email],
#                 )
#                 email.send(fail_silently=False)
#                 messages.success(request, 'Account successfully created')
#                 return render(request, 'authentication/register.html')

#         return render(request, 'authentication/register.html')






class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        context = {'fieldValues': request.POST}

        # Validate input
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'authentication/register.html', context)

        if len(password) < 6:
            messages.error(request, 'Password too short.')
            return render(request, 'authentication/register.html', context)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'authentication/register.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'authentication/register.html', context)

        # Create user
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        # Create user preference with default currency "INR"
        UserPreference.objects.create(user=user, currency='INR')

        # Send activation email
        try:
            current_site = get_current_site(request)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            link = reverse('activate', kwargs={'uidb64': email_body['uid'], 'token': email_body['token']})
            activate_url = f"http://{current_site.domain}{link}"

            email_subject = 'Activate your account'
            email_message = f"Hi {user.username},\n\nPlease click the link below to activate your account:\n{activate_url}"

            email = EmailMessage(email_subject, email_message, 'noreply@semycolon.com', [email])
            email.send(fail_silently=False)

            messages.success(request, 'Account successfully created. Check your email for activation link.')
            return redirect('login')  # Redirect to login page after successful registration
        except Exception as e:
            messages.error(request, f"Error sending activation email: {str(e)}")
            user.delete()  # Rollback user creation if email fails
            return render(request, 'authentication/register.html', context)
        



class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('dashboard')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
    

















class PasswordResetView(View):
    def post(self, request):
        email = request.POST.get('email')
        print("Email:", email)
        if email:
            # Handle email input form submission
            try:
                user = User.objects.get(email=email)
                print("User:", user)
                subject = 'Password Reset Requested'
                email_template_name = 'authentication/password_reset_email.html'
                # Generate password reset token
                password_reset_token = PasswordResetTokenGenerator().make_token(user)
                print("Password Reset Token:", password_reset_token)
                uidb64 = urlsafe_base64_encode(force_bytes((user.pk)))
                print("uidb64:", uidb64)
                # Pass uidb64 and token to the template
                email_body = {
                    'user': user,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'Website',
                    'protocol': request.scheme,
                    'uidb64': uidb64,
                    'token': password_reset_token,
                }
                link = reverse('password_reset_confirm', kwargs={'uidb64': email_body['uidb64'], 'token': email_body['token']})
                password_reset_url = f"http://{request.META['HTTP_HOST']}{link}"
                print("Password Reset URL:", password_reset_url)
                email_subject = 'Password Reset Requested'
                email_message = f"Hi {user.username},\n\nPlease click the link below to reset your password:\n{password_reset_url}"
                email = EmailMessage(email_subject, email_message, 'noreply@semycolon.com', [email])
                email.send(fail_silently=False)
                messages.success(request, 'Password reset email sent successfully')
                return render(request, 'authentication/password_reset_done.html')
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist')
                return render(request, 'authentication/password_reset_form.html')
        else:
            # Handle "Forgot password?" link click
            return render(request, 'authentication/password_reset_form.html')





class PasswordResetDoneView(View):
    def post(self, request):
        return render(request, 'authentication/password_reset_done.html')

class PasswordResetConfirmView(View):
    def post(self, request):
        return render(request, 'authentication/password_reset_confirm.html')

class PasswordResetCompleteView(View):
    def post(self, request):
        return render(request, 'authentication/password_reset_complete.html')
