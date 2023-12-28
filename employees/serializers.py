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


class viewAllUserSerializer(serializers.Serializer):
    employee_id = serializers.CharField()
    name = serializers.CharField()
    user_role = serializers.CharField()
    designation = serializers.CharField()
    department = serializers.CharField()
    product = serializers.CharField(required=False)



class viewUserIndvSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    employee_id = serializers.CharField()
    email = serializers.CharField()
    age = serializers.CharField()
    gender = serializers.CharField()
    mobile_number = serializers.CharField()
    alternate_mobile_number = serializers.CharField()
    blood_group = serializers.CharField()
    date_of_birth = serializers.CharField()
    disability = serializers.CharField()
    employee_status = serializers.CharField()
    marital_status = serializers.CharField()
    nationality = serializers.CharField()
    emp = serializers.CharField(required=False)


    class Meta:
        model = employee_official
        fields = '__all__'


class deleteUserSerializer(serializers.Serializer):
    employee_id = serializers.CharField()



def dynamic_serializer(model_class):
    class dynamicSeralizer(serializers.ModelSerializer):
        # password = serializers.CharField(read_only=True)
        class Meta:
            model = model_class
            exclude = ['emp']
    return dynamicSeralizer


class UserAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)
    class Meta:
        model = UserAccount
        exclude = ['employee_id', 'email', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser', 'visibility', 'updated_at']