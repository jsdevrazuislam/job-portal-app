from django.shortcuts import render, redirect
from joblisting.views import get_footer_data
from .forms import UserRegisterForm, PasswordResetConfirmForm, PasswordResetRequestForm
from django.contrib.auth import login as loginUser, authenticate, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from django.contrib import messages

User = get_user_model()

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_link = f"{request.build_absolute_uri('/auth/verify-email/')}{uid}/{token}/"
    email_subject = "Verify Your Email"
    email_message = f"Click the link to verify your email: {verification_link}"

    send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [user.email])



def login(request):
    footer_data = get_footer_data()
    if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                loginUser(request, user)
                messages.success(request, 'Login Successfully')
                return redirect('home') 
            else:
                messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html', footer_data)

def register(request):
    footer_data = get_footer_data()
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            form.save()
            send_verification_email(user, request)
            return redirect('registration/verification_sent.html')
        else:
            print(form.errors)
    context = {**footer_data, "form": form} 
    return render(request, 'register.html', context)

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"message": "Logout Successfully"}, status=200)
    else:
        return JsonResponse({"message": "Invalid Request"}, status=400)

def verify_email_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Verify Complete. Please login now!')
        return redirect('login')  
    else:
        return render(request, "registration/verification_failed.html")

def reset_password(request):
     footer_data= get_footer_data()
     if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = f"{request.build_absolute_uri('/auth/password-reset-confirm/')}{uid}/{token}/"
            email_subject = "Password Reset Request"
            email_message = render_to_string('password_reset_email.html', {'reset_link': reset_link})
            send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            return redirect('reset_password_done')

     form = PasswordResetRequestForm()
     return render(request, 'registration/password_reset_form.html', {**footer_data, "form": form})

def reset_password_done(request):
    return render(request, 'registration/password_reset_done.html')

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()
                return redirect('login')
        else:
            form = PasswordResetConfirmForm()
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'registration/password_reset_invalid.html')
