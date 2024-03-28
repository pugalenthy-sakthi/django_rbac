from django.db import models
from auth_app.models import Base
from policy_app.models import Policy
from enum import Enum as pyenum


class APIMethods(pyenum):
  
  GET = 1
  POST = 2
  PUT = 3
  DELETE = 4
  

class API(Base):
  
  api_name = models.CharField(max_length = 80, null = False, blank = False, unique = True)
  api_path = models.TextField()
  method = models.IntegerField()
  policies = models.ManyToManyField(Policy,related_name='apis_list')
