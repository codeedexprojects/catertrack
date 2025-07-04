# users/urls.py

from django.urls import path
from users.views import *

urlpatterns = [
    path('create-user/', createuserview.as_view(), name='user-create'),#admin-create user
    path('signin/', SigninView.as_view(), name='signin'),#login for all users
    path('update/users/', UserUpdateView.as_view(), name='user-update'), #update user
    path('users/me/', UserMeView.as_view(), name='user-details'), #user profile get
    path('staff/details/create/', StaffDetailsCreateView.as_view(), name='staff-details-create'), #staff details create
    path('staff-details/', StaffDetailsView.as_view(), name='user-detail-by-role'),#staff single detail

]