from django.urls import path
from . import views

urlpatterns = [
    path('service/create',view=views.create_service,name='create_service'),
    path('api/list',view=views.get_all_apis,name='list_all_api'),
]
