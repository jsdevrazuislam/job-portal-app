from django.urls import path
from .views import login, register, reset_password, reset_password_done, password_reset_confirm_view, user_logout, verify_email_view


urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path("logout", user_logout, name="logout"),
    path('password_reset/', reset_password, name='password_reset'),
    path('password_reset/done/', reset_password_done, name='reset_password_done'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path("verify-email/<uidb64>/<token>/", verify_email_view, name="verify_email"),


]