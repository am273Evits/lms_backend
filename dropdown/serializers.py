from rest_framework import serializers


class dropdownOptionSerializers(serializers.Serializer):
    title = serializers.ListField()


class employeesAllTablesSerializer(serializers.Serializer):
    tables = serializers.ListField()