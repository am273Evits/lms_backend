from rest_framework import serializers
from account.models import UserAccount


class dropdownOptionSerializers(serializers.Serializer):
    title = serializers.ListField()


class employeesAllTablesSerializer(serializers.Serializer):
    tables = serializers.ListField()


