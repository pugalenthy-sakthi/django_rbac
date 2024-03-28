
from django.urls import path,include

urlpatterns = [
  path('auth/',include('auth_app.urls')),
  path('dev/',include('dev_app.urls')),
  path('policy/',include('policy_app.urls'))
]
