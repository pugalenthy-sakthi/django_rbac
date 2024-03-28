from django.http import HttpRequest
from django_rbac.common import Responses,response_sender
from http import HTTPStatus
from .serializers import ServiceSerializer
from service_app.models import API,APIMethods
import json
import traceback

def create_service(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      json_data = json.loads(request.body)
      service_data = ServiceSerializer(data=json_data)
      if not service_data.is_valid() :  
        return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
      service_data = service_data.data
      api = API()
      api.api_name = service_data['api_name']
      api.api_path = service_data['api_path']
      api.method = APIMethods[service_data['method']].value
      api.save()
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
    except json.JSONDecodeError as e:
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      print(e)
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else : 
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  
def get_all_apis(request:HttpRequest):
  
  if request.method == 'GET':
    try:
      api_list = API.objects.all()
      api_list = [
        {
          'api_id' : api.id,
          'api_path' : api.api_path,
          'api_name' : api.api_name,
          'api_method' : APIMethods(api.method).name
        }
        for api in api_list
      ]
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=api_list,http=HTTPStatus.OK)
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)