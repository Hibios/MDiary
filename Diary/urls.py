from django.urls import path
from django.contrib.auth import views

from . import views as app_views

from .forms import UserLoginForm, PasswordResetUserForm, SetPasswordUserForm

app_name = 'Diary'
urlpatterns = [
    path('', app_views.index, name='profile'),
    path('login', views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('password_reset', views.PasswordResetView.as_view(form_class=PasswordResetUserForm), name='password_reset'),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(form_class=SetPasswordUserForm),
         name="password_reset_confirm"),
    path('reset_password_complete/', views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('register', app_views.register_request, name='register'),
    path('edit_profile', app_views.update_profile, name='edit_profile'),

    path('events', app_views.show_events, name='events'),
    path('events/add_event', app_views.add_event, name='add_event'),
    path('events/<int:year>/<int:month>/<int:day>/<slug:event>/', app_views.event_detail, name='event_detail'),
    path('events/<int:year>/<int:month>/<int:day>/<slug:event>/edit_event', app_views.update_event, name='edit_event'),
]
