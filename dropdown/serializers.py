from rest_framework import serializers
from account.models import UserAccount


class dropdownOptionSerializers(serializers.Serializer):
    title = serializers.ListField()


class employeesAllTablesSerializer(serializers.Serializer):
    tables = serializers.ListField()



class CommonDropdownSerializer(serializers.Serializer):
    id = serializers.CharField()
    value = serializers.CharField()

# class dropdown_designationSerializer(serializers.Serializer):
#     designation_id = serializers.CharField()
#     designation_name = serializers.CharField()

# class dropdown_programSerializer(serializers.Serializer):
#     program_id = serializers.CharField()
#     program_name = serializers.CharField()

# class dropdown_employee_statusSerializer(serializers.Serializer):
#     employee_status_id = serializers.CharField()
#     employee_status_name = serializers.CharField()

# class employee_List_Serializer(serializers.Serializer):
#     employee_id = serializers.CharField()
#     employee_name = serializers.CharField()