from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import EditProfileView

urlpatterns = [
    # Register (custom view)
    path('register/', views.register_view, name='register'),
    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    # Login / Logout (Django's built-in views)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    # Optional: User profile (custom view)
    path('profile/', views.profile, name='profile'),

    # Password reset workflow
    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
]
