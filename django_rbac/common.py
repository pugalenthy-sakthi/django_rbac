from http import HTTPStatus
from django.http import JsonResponse
import bcrypt
import jwt
from datetime import datetime,timedelta,UTC
import uuid
from django.conf import settings

class Responses:
  
  INVALID_DATA = 'Invalid Data'
  DUPLICATE_DATA = 'Data Already Exist'
  CREATE_RESPONSE = 'Data Created Successfully'
  SERVER_ERROR = 'OOPS!'
  INVALID_REQUEST = 'Invalid Request'
  NOT_FOUND = 'The Given Data Not Found'
  SUCCESS_RESPONSE = 'Success'
  INVALID_CREDENTIALS = 'Invalid Credentials'
  FORBIDDEN = 'Forbidden'
  API_NOT_FOUND = 'Api Not Found'
  UPDATED_RESPONSE = 'Updated'
  DELETED_RESPONSE = 'Deleted'

def response_sender(message,data,http:HTTPStatus):
  
  body = {
    'http_status':http.phrase,
    'message':message,
    'data':data
  }
  
  return JsonResponse(data = body,status = http.value)

def gethashpwd(pwd):
  
  return (bcrypt.hashpw(bytes(pwd,'utf-8'),bcrypt.gensalt(rounds=12))).decode('utf-8')


def checkpwd(pwd:str,hpwd:str):
  
  return bcrypt.checkpw(hashed_password=hpwd.encode('utf-8'),password=pwd.encode('utf-8'))



class JWT:
  
  
  def get_jwt(subject,payload = None):
    
    jwt_claims = {
      'exp' : datetime.now(UTC) + timedelta(seconds=float(settings.JWT_TOKEN_TIME)),
      'sub' : subject,
      'iat' : datetime.now(UTC)
    }
    
    if payload is None : 
      payload = jwt_claims
    
    payload.update(jwt_claims)
    
    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.JWT_ALGO)
  
  
  def get_jwt_refresh(subject,payload = None):
    
    jwt_claims = {
      'exp' : datetime.now(UTC) + timedelta(seconds=float(settings.JWT_REFRESH_TIME)),
      'sub' : subject,
      'iat' : datetime.now(UTC)
    }
    
    if payload is None : 
      payload = jwt_claims
      
    payload.update(jwt_claims)
    
    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.JWT_ALGO)
  
  def verify_jwt_token(token):
    try:
      payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO],verify=True)
      return payload  
    except jwt.ExpiredSignatureError as e:
      return None
    except jwt.InvalidTokenError as e:
      return None
    except Exception as e:
      return None
    
def get_random_id():
    return uuid.uuid4().hex