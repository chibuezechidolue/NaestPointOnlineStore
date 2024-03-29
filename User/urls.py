from django.shortcuts import redirect
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name='user/login.html'), name="login-page"),
    # path("login/", views.login_page, name="login-page"),
    path("register/", views.register_page, name="register-page"),
    path("profile/", views.user_profile, name="user-profile"),
    path("profile/<option>", views.user_profile, name="user-profile-edit"),
    path("profile/change-password/",views.ChangePasswordView.as_view(extra_context={"change_password":True},success_url=reverse_lazy("user-profile")),name="change-password"),
    # path("logout/", views.logout_page, name="logout-page"),
    path('logout/',auth_views.LogoutView.as_view(),name="logout-page"),
     path('password-reset/',auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"),name='password-reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_done.html"),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_confirm.html"),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_complete.html"),name='password_reset_complete'),
    
    
]