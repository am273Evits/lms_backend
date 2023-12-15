from rest_framework import serializers
from .models import *


class getAssociatesSerializers(serializers.Serializer):
    employee_id = serializers.CharField()
    name = serializers.CharField()
    user_role = serializers.CharField()


# class getTableFieldsSerializer(serializers.Serializer):
#     field = serializers.CharField()
#     type = serializers.CharField()


# class employee_basicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = employee_basic
#         fields = '__all__'

    # def validate(self, attrs):
    #     return super().validate(attrs)
    
    # def create(self, validated_data):
    #     emp=employee_basic()
    #     emp.employee_status=""
    #     return super().create(validated_data)

class employee_officialSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee_official
        fields = '__all__'