from rest_framework import serializers


class PolicySerializer(serializers.Serializer):
  
  policy_name = serializers.CharField()
  
class PolicyApiSerializer(serializers.Serializer):
  
  policy_id = serializers.IntegerField()
  apis_id = serializers.ListField(child = serializers.IntegerField())
  
class PolicyUserSerializer(serializers.Serializer):
  
  policy_id = serializers.IntegerField()
  users_id = serializers.ListField(child = serializers.IntegerField())