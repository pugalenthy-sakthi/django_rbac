import traceback
from django.http import HttpRequest
from django_rbac.common import Responses,response_sender
from http import HTTPStatus
import json
from .serializers import PolicySerializer,PolicyApiSerializer,PolicyUserSerializer
from .models import Policy
from service_app.models import APIMethods,API
from auth_app.models import Users
from django.db import transaction
from rest_framework import serializers



def create_policy(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      json_data = json.loads(request.body)
      policy_data = PolicySerializer(data=json_data)
      if not policy_data.is_valid() : 
        return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
      policy_data = policy_data.data
      policy = Policy.objects.filter(policy_name = policy_data['policy_name']).first()
      if policy is not None:
        return response_sender(message=Responses.DUPLICATE_DATA,data={'policy_name':policy_data['policy_name']},http=HTTPStatus.CONFLICT)
      policy = Policy()
      policy.policy_name = policy_data['policy_name']
      policy.save()
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
    except json.JSONDecodeError as e:
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  
def get_all_policies(request:HttpRequest):
  
  if request.method == 'GET':
    try:
      policy_list = Policy.objects.all()
      policy_list = [
        {
          'policy_id' : policy.id,
          'policy_name' : policy.policy_name,
          'services' :[
            {
              'service_id' : api.id,
              'service_name' : api.api_name,
              'service_path' : api.api_path,
              'service_method' : APIMethods(api.method).name
            }
            for api in policy.apis_list.all()  
          ]
        }
        for policy in policy_list
      ]
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=policy_list,http=HTTPStatus.OK)
    except json.JSONDecodeError as e:
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      print(e)
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  
def update_policy_api(request:HttpRequest):
  
  if request.method == 'PUT':
    try:
      json_data = json.loads(request.body)
      policy_api_data = PolicyApiSerializer(data=json_data)
      if not policy_api_data.is_valid() : 
        return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
      policy_api_data = policy_api_data.data
      with transaction.atomic():
        policy = Policy.objects.filter(id = policy_api_data['policy_id']).first()
        if policy is None:
          return response_sender(message=Responses.INVALID_DATA,data={'policy_id':policy_api_data['policy_id']},http=HTTPStatus.BAD_REQUEST)
        for api_id in policy_api_data['apis_id']:
          api = API.objects.filter(id = api_id).first()
          if api is None:
            raise serializers.ValidationError
          policy.apis_list.add(api)
        policy.save()
      transaction.commit()
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=None,http=HTTPStatus.OK)
    except serializers.ValidationError as e:
      transaction.rollback()
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except json.JSONDecodeError as e:
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      traceback.print_exception(e)
      transaction.rollback()
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  

def update_policy_user(request:HttpRequest):
  
  if request.method == 'PUT':
    try:
      json_data = json.loads(request.body)
      policy_user_data = PolicyUserSerializer(data=json_data)
      if not policy_user_data.is_valid() : 
        return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
      policy_user_data = policy_user_data.data
      with transaction.atomic():
        policy = Policy.objects.filter(id = policy_user_data['policy_id']).first()
        if policy is None:
          return response_sender(message=Responses.INVALID_DATA,data={'policy_id':policy_user_data['policy_id']},http=HTTPStatus.BAD_REQUEST)
        for user_id in policy_user_data['users_id']:
          user = Users.objects.filter(id = user_id).first()
          if user is None:
            raise serializers.ValidationError
          policy.users_list.add(user)
        policy.save()
      transaction.commit()
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=None,http=HTTPStatus.OK)
    except serializers.ValidationError as e:
      transaction.rollback()
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except json.JSONDecodeError as e:
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      traceback.print_exception(e)
      transaction.rollback()
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)