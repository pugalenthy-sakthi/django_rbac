from django.db import models
from auth_app.models import Base,Users


class Policy(Base):
  
  policy_name = models.CharField(max_length = 100, null = False, blank = False,unique = True)
  
  users_list = models.ManyToManyField(Users,related_name='policies')
  
