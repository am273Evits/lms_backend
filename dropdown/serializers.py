from rest_framework import serializers
from account.models import UserAccount


class dropdownOptionSerializers(serializers.Serializer):
    title = serializers.ListField()


class employeesAllTablesSerializer(serializers.Serializer):
    tables = serializers.ListField()


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
        exclude = ['employee_id', 'email', 'last_login', 'is_active', 'is_admin', 'is_staff', 'is_superuser', 'visibility']