from .common import JWT,response_sender,Responses
from django.http import HttpRequest
from http import HTTPStatus
from auth_app.models import Activity
import traceback

open_paths = [
  '/auth/login',
  '/auth/signup',
  '/favicon.ico' 
]

class SecurityMiddleware:
  
  def __init__(self,get_response) :
    
    self.get_response = get_response
    
  def __call__(self, request:HttpRequest) :
    
    if request.path in open_paths :
      return self.get_response(request)
    if 'Authorization' not in request.headers:
      return response_sender(Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)
    token = request.headers['Authorization']
    try:
      data = JWT.verify_jwt_token(token)
      if data == None :
        return response_sender(Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)
      session_id = data['sub']
      activity = Activity.objects.filter(session_id = session_id).first()
      if activity.logout_at != None:
        return response_sender(Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)
      if activity.user.isdev :
        return self.get_response(request)
      user = activity.user
      flag = False
      for policy in user.policies.all():
        for api in policy.apis_list.all():
          if api.api_path == request.path:
            flag = True
            break
        if flag:
            break
      if flag : 
        return self.get_response(request)
      return response_sender(Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)
      
    except Exception as e:
      return response_sender(Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)

  
  def process_exception(self,request,exception):    
    return response_sender(Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)