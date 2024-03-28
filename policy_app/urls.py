from django.urls import path
from . import views

urlpatterns = [
    path('create',view=views.create_policy,name='create_policy'),
    path('get/all',view=views.get_all_policies,name='get_all_policies'),
    path('add/api',view=views.update_policy_api,name='add_policy_with_api'),
    path('add/user',view=views.update_policy_user,name='add_policy_with_user')
]
