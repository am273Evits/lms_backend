from rest_framework import serializers
from django.db.models import Q
from .models import ev_services
from account.views import getServiceId

class servicesSerializer(serializers.ModelSerializer):
    # service_id = serializers.CharField()
    # print('working')
    class Meta:
        model = ev_services
        exclude = ['price_for_mou']

    def validate(self, attrs):
        

        marketplace = attrs.get('marketplace')
        country = attrs.get('country')
        services = attrs.get('services')
        static_service_fees = attrs.get('static_service_fees')
        commission_fees = attrs.get('commission_fees')
        commission_service_fees = attrs.get('commission_service_fees')
        service_currency = attrs.get('service_currency')
        price_for_mou = ''
        # print('marketplace',attrs)

        if commission_fees == True:
            price_for_mou = f"Higher of ({service_currency.upper()} {static_service_fees} or {commission_service_fees}% of sales)"
            condition = Q(services = services) & Q(static_service_fees = static_service_fees) & Q(commission_service_fees = commission_service_fees) & Q(price_for_mou = price_for_mou)
            condition2 = Q(services = services) &  Q(price_for_mou = price_for_mou)
        else:
            price_for_mou = static_service_fees
            condition = Q(services = services) & Q(static_service_fees = static_service_fees) & Q(price_for_mou = price_for_mou)
            condition2 = Q(services = services) &  Q(price_for_mou = price_for_mou)


        ev_ser =  ev_services.objects.filter(condition)
        ev_ser2 =  ev_services.objects.filter(condition2)

        # valE = ()
        if ev_ser.exists() or ev_ser2.exists():
            raise serializers.ValidationError('Service already exists')
        if marketplace is None:
            raise serializers.ValidationError('marketplace is required')
        if country is None:
            raise serializers.ValidationError('country is required')
        if services is None:
            raise serializers.ValidationError('services is required')
        if services is None:
            raise serializers.ValidationError('services is required')
        if static_service_fees is None:
            raise serializers.ValidationError('static service fees is required')
        if commission_fees == True:
            if commission_service_fees is None:
                raise serializers.ValidationError('commission service fees is required')
        if service_currency is None:
            raise serializers.ValidationError('service currency is required')
        
        attrs['price_for_mou'] = price_for_mou
        return attrs


    def create(self, validated_data):
        validated_data['service_id'] = getServiceId() 
        data = ev_services.objects.create(**validated_data)
        return data


class viewServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ev_services
        exclude = ['visibility']


class viewAllServicesSerializer(serializers.ModelSerializer):

    # visibility = serializers.CharField(read_only=True)

    class Meta:
        model = ev_services
        exclude = ['visibility']

    def validate(self, attrs):

        services = attrs.get('services')
        commission_fees = attrs.get('commission_fees')
        static_service_fees = attrs.get('static_service_fees')
        commission_service_fees = attrs.get('commission_service_fees')
        service_currency = attrs.get('service_currency')
        
        if commission_fees is None:
            raise serializers.ValidationError('commission_fees fields is required true/false')
        if static_service_fees is None:
            raise serializers.ValidationError('static_service_fees fields is required')
        if commission_service_fees is None:
            raise serializers.ValidationError('commission_service_fees fields is required')
        if service_currency is None:
            raise serializers.ValidationError('service_currency fields is required')
        if services is None:
            raise serializers.ValidationError('services fields is required')
            

        if commission_fees == True:
            price_for_mou = f"Higher of ({service_currency.upper()} {static_service_fees} or {commission_service_fees}% of sales)"
            condition = Q(services = services) & Q(static_service_fees = static_service_fees) & Q(commission_service_fees = commission_service_fees) & Q(price_for_mou = price_for_mou)
            condition2 = Q(services = services) &  Q(price_for_mou = price_for_mou)
        else:
            price_for_mou = static_service_fees
            condition = Q(services = services) & Q(static_service_fees = static_service_fees) & Q(price_for_mou = price_for_mou)
            condition2 = Q(services = services) &  Q(price_for_mou = price_for_mou)

        ev_ser =  ev_services.objects.filter(condition)
        ev_ser2 =  ev_services.objects.filter(condition2)

        if ev_ser.exists() or ev_ser2.exists():
            raise serializers.ValidationError('Service already exists')
        
        attrs['price_for_mou'] = price_for_mou
        return attrs
