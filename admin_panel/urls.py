from django.urls import path
from admin_panel.views import *
from users.views import AdminUserListView,AdminUserUpdateView

urlpatterns =[
    path('login/', AdminLoginView.as_view(), name='admin-login'),#admin login
    path('base-fares/', BaseFareCreateView.as_view(), name='base-fare-create'), #base fare create
    path('list-base-fares/', BaseFareListView.as_view(), name='base-fare-list'), #base fare list
    path('base-fares/update/<str:fare_type>/', BaseFareUpdateView.as_view(), name='base-fare-update'), #base fare update
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:id>/update/', AdminUserUpdateView.as_view(), name='admin-user-update'),


]