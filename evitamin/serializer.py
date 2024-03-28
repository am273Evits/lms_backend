from rest_framework import serializers
from django.db.models import Q
# from .models import ev_services
# from account.views import getServiceId
from leads.models import *




class CreateServicesCommercialsSerializer(serializers.Serializer):
    segment = serializers.IntegerField()
    service = serializers.IntegerField()
    marketplace = serializers.IntegerField()
    program = serializers.IntegerField()
    sub_program = serializers.IntegerField(required=False)
    # service_name = serializers.CharField()
    commercials = serializers.ListField()

    def validate(self, attrs):

        # print('validate working')

        segment = attrs.get('segment')
        service = attrs.get('service')
        marketplace = attrs.get('marketplace')
        program = attrs.get('program')
        sub_program = attrs.get('sub_program')
        # service_name = attrs.get('service_name')
        commercials = attrs.get('commercials')

        # print('printed from the be', segment, service, marketplace, program,sub_program, commercials)
        
            # if not isinstance(c.get('price'), int):
            #     raise serializers.ValidationError('price should be a number')
        if not isinstance(segment, int):
            raise serializers.ValidationError('segment should be a number')
        if not isinstance(service, int):
            raise serializers.ValidationError('services should be a number')
        if not isinstance(marketplace, int):
            raise serializers.ValidationError('marketplace should be a number')
        if not isinstance(program, int):
            raise serializers.ValidationError('program should be a number')
        if sub_program != None:
            if not isinstance(sub_program, int):
                raise serializers.ValidationError('sub_program should be a number')
        
        for c in commercials:
            if not c or c == None:
                raise serializers.ValidationError('commercial is required field')
            
        # if not service_name or service_name == None or service_name == '':
        #     raise serializers.ValidationError('price for mou is required field')

        # marketplace = Marketplace.objects.filter(id = marketplace)
        # if not marketplace.exists():
        #     raise serializers.ValidationError('marketplace id is incorrect')
        
        return attrs

    def create(self, validated_data):
        segment = Segment.objects.get(id=validated_data['segment'])
        service = Service.objects.get(id=validated_data['service'])
        marketplace = Marketplace.objects.get(id=validated_data['marketplace'])
        program = Program.objects.get(id=validated_data['program'])
        sub_program = Sub_Program.objects.get(id=validated_data['sub_program'])
        commercials = validated_data['commercials']

        # del validated_data['commercials']

        # print('segment',segment)
        # print('service',service)
        # print('marketplace',marketplace)
        # print('program',program)
        # print('sub_program',sub_program)
        # print('commercials',commercials)
        # print('validated_data',validated_data)

        services_and_commercials = Services_and_Commercials.objects.create(**{'segment': segment, 'service': service, 'marketplace': marketplace, 'program': program, 'sub_program': sub_program})

        # services_and_commercials.commercisals.set(commercials)

        # print(services_and_commercials)

        # marketplace = Marketplace.objects.filter(id = marketplace).first()

        # service = Services.objects.create(service_name = service_name)

    #     # marketplace.service.add(service)

        for c in commercials:
            commercial = Commercials.objects.create(**{'commercials' : c.strip() })
            services_and_commercials.commercials.add(commercial)

    #     # commercial = service.commercials

    #     # marketplace = Marketplace.objects.filter(id = marketplace_id).first()
    #     # services = Services.objects.create(**{'service_name': service_name,'marketplace_id': marketplace})

    #     # for c in commercial:
    #     #     Commercials.objects.create(**{'service_id': services,'price': c.get('price'), 'commission': c.get('commission'), 'price_for_mou': c.get('price_for_mou')})

        return validated_data
    



class CreateServicesCommercialsSerializer_NSP(serializers.Serializer):
    segment = serializers.IntegerField()
    service = serializers.IntegerField()
    marketplace = serializers.IntegerField()
    program = serializers.IntegerField()
    # sub_program = serializers.IntegerField(required=False)
    commercials = serializers.ListField()

    def validate(self, attrs):

        segment = attrs.get('segment')
        service = attrs.get('service')
        marketplace = attrs.get('marketplace')
        program = attrs.get('program')
        # sub_program = attrs.get('sub_program')
        commercials = attrs.get('commercials')

        if not isinstance(segment, int):
            raise serializers.ValidationError('segment should be a number')
        if not isinstance(service, int):
            raise serializers.ValidationError('services should be a number')
        if not isinstance(marketplace, int):
            raise serializers.ValidationError('marketplace should be a number')
        if not isinstance(program, int):
            raise serializers.ValidationError('program should be a number')
        # if sub_program != None:
        #     if not isinstance(sub_program, int):
        #         raise serializers.ValidationError('sub_program should be a number')
        
        for c in commercials:
            if not c or c == None:
                raise serializers.ValidationError('commercial is required field')
            
        return attrs

    def create(self, validated_data):

        print('validated_data',validated_data)

        segment = Segment.objects.get(id=validated_data['segment'])
        service = Service.objects.get(id=validated_data['service'])
        marketplace = Marketplace.objects.get(id=validated_data['marketplace'])
        program = Program.objects.get(id=validated_data['program'])
        # sub_program = Sub_Program.objects.get(id=validated_data['sub_program'])
        commercials = validated_data['commercials']

        services_and_commercials = Services_and_Commercials.objects.create(**{'segment': segment, 'service': service, 'marketplace': marketplace, 'program': program})

        for c in commercials:
            commercial = Commercials.objects.create(**{'commercials' : c.strip() })
            services_and_commercials.commercials.add(commercial)

        return validated_data



class ViewServiceAndCommercialSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    # segment = serializers.DictField()
    # service = serializers.DictField()
    # marketplace = serializers.DictField()
    # program = serializers.DictField()
    # sub_program = serializers.DictField()
    commercials = serializers.ListField()
    type = serializers.CharField()


class ViewServiceAndCommercial_NC_Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    segment = serializers.DictField()
    service = serializers.DictField()
    marketplace = serializers.DictField()
    program = serializers.DictField()
    sub_program = serializers.DictField()
    # commercials = serializers.DictField()





















# class servicesSerializer(serializers.ModelSerializer):
#     # service_id = serializers.CharField()
#     # print('working')
#     class Meta:
#         model = ev_services
#         exclude = ['price_for_mou']

#     def validate(self, attrs):
        

#         marketplace = attrs.get('marketplace')
#         country = attrs.get('country')
#         services = attrs.get('services')
#         static_service_fees = attrs.get('static_service_fees')
#         commission_fees = attrs.get('commission_fees')
#         commission_service_fees = attrs.get('commission_service_fees')
#         service_currency = attrs.get('service_currency')
#         price_for_mou = ''
#         # print('marketplace',attrs)

#         if commission_fees == True:
#             price_for_mou = f"Higher of ({service_currency.upper()} {static_service_fees} or {commission_service_fees}% of sales)"
#             condition = Q(services = services) & Q(static_service_fees = static_service_fees) & Q(commission_service_fees = commission_service_fees) & Q(price_for_mou = price_for_mou)
#             condition2 = Q(services = services) &  Q(price_for_mou = price_for_mou)
#         else:
#             price_for_mou = static_service_fees
#             condition = Q(services = services) & Q(static_service_fees = static_service_fees) & Q(price_for_mou = price_for_mou)
#             condition2 = Q(services = services) &  Q(price_for_mou = price_for_mou)


#         ev_ser =  ev_services.objects.filter(condition)
#         ev_ser2 =  ev_services.objects.filter(condition2)

#         # valE = ()
#         if ev_ser.exists() or ev_ser2.exists():
#             raise serializers.ValidationError('Service already exists')
#         if marketplace is None:
#             raise serializers.ValidationError('marketplace is required')
#         if country is None:
#             raise serializers.ValidationError('country is required')
#         if services is None:
#             raise serializers.ValidationError('services is required')
#         if services is None:
#             raise serializers.ValidationError('services is required')
#         if static_service_fees is None:
#             raise serializers.ValidationError('static service fees is required')
#         if commission_fees == True:
#             if commission_service_fees is None:
#                 raise serializers.ValidationError('commission service fees is required')
#         if service_currency is None:
#             raise serializers.ValidationError('service currency is required')
        
#         attrs['price_for_mou'] = price_for_mou
#         return attrs


#     def create(self, validated_data):
#         validated_data['service_id'] = getServiceId() 
#         data = ev_services.objects.create(**validated_data)
#         return data


# class viewServicesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ev_services
#         exclude = ['visibility', 'service_currency', 'commission_service_fees', 'commission_fees', 'static_service_fees']


# class viewAllServicesSerializer(serializers.ModelSerializer):

#     # visibility = serializers.CharField(read_only=True)

#     class Meta:
#         model = ev_services
#         exclude = ['visibility']

#     def validate(self, attrs):

#         services = attrs.get('services')
#         commission_fees = attrs.get('commission_fees')
#         static_service_fees = attrs.get('static_service_fees')
#         commission_service_fees = attrs.get('commission_service_fees')
#         service_currency = attrs.get('service_currency')
        
#         if commission_fees is None:
#             raise serializers.ValidationError('commission_fees fields is required true/false')
#         if static_service_fees is None:
#             raise serializers.ValidationError('static_service_fees fields is required')
#         if commission_service_fees is None:
#             raise serializers.ValidationError('commission_service_fees fields is required')
#         if service_currency is None:
#             raise serializers.ValidationError('service_currency fields is required')
#         if services is None:
#             raise serializers.ValidationError('services fields is required')
            

#         if commission_fees == True:
#             price_for_mou = f"Higher of ({service_currency.upper()} {static_service_fees} or {commission_service_fees}% of sales)"
#             condition = Q(services = services) & Q(static_service_fees = static_service_fees) & Q(commission_service_fees = commission_service_fees) & Q(price_for_mou = price_for_mou)
#             condition2 = Q(services = services) &  Q(price_for_mou = price_for_mou)
#         else:
#             price_for_mou = static_service_fees
#             condition = Q(services = services) & Q(static_service_fees = static_service_fees) & Q(price_for_mou = price_for_mou)
#             condition2 = Q(services = services) &  Q(price_for_mou = price_for_mou)

#         ev_ser =  ev_services.objects.filter(condition)
#         ev_ser2 =  ev_services.objects.filter(condition2)

#         if ev_ser.exists() or ev_ser2.exists():
#             raise serializers.ValidationError('Service already exists')
        
#         attrs['price_for_mou'] = price_for_mou
#         return attrs
