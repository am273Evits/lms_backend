from rest_framework import serializers


class dropdownOptionSerializers(serializers.Serializer):
    title = serializers.CharField()


