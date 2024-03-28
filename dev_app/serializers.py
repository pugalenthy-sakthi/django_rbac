from rest_framework import serializers
from service_app.models import APIMethods


class ServiceSerializer(serializers.Serializer):
  
  api_name = serializers.CharField()
  api_path = serializers.CharField()
  method = serializers.CharField()
  
  def validate(self, attrs):
    
    method = attrs.get('method')
    keys_list = [member.name for member in APIMethods]
    
    if method not in keys_list:
      raise serializers.ValidationError
    
    return attrs
    
  