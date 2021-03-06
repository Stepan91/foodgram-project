from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
                template_name='registration/password_change_form.html',
                success_url=reverse_lazy('password_change_done')
                ),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
                template_name='registration/password_change_done.html'
                ),
         name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
                template_name='registration/password_reset.html'
                ),
         name='password_reset'),
    path('password-reset/<uidb64>/<str:token>/',
         auth_views.PasswordResetConfirmView.as_view(
                template_name='registration/password_reset_confirm.html'
                ),
         name='password_reset_confirm'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
                template_name='registration/password_reset_done.html'
                ),
         name='password_reset_done'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
                template_name='registration/password_reset_complete.html'
                ),
         name='password_reset_complete'),
    path('user_logout/', auth_views.LogoutView.as_view(
                template_name='registration/logout.html'
                ),
         name='user_logout')
]
