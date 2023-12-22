from rest_framework import serializers
from .models import *
from dropdown.models import *
from evitamin.models import *
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError

from records.models import lead_status_record

from account.views import getLeadId


class lead_managerBlSerializer(serializers.Serializer):
    lead_id = serializers.CharField()
    requester_name = serializers.CharField()
    service_category = serializers.CharField()
    lead_status = serializers.CharField()


class BusinessDevelopmentLeadSerializer(serializers.Serializer):
    lead_id = serializers.CharField() 
    service_category = serializers.CharField() 
    associate = serializers.CharField() 
    lead_status = serializers.CharField() 
    requester_name = serializers.CharField() 
    phone_number = serializers.CharField() 
    email_id = serializers.CharField()


class allIdentifiersSerializer(serializers.ModelSerializer):
    class Meta:
        model = all_identifiers
        fields = '__all__'

# class businessIdentifiersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = business_identifiers
#         exclude = ['lead_id']

# class commentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = comment
#         exclude = ['lead_id']

# class contactPreferenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = contact_preference
#         fields = '__all__'

# class followupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = followup
#         exclude = ['lead_id']

# class sellerAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = seller_address
#         exclude = ['lead_id']

# class serviceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = service
#         exclude = ['lead_id']

# class websiteStoreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = website_store
#         exclude = ['lead_id']



def dynamic_serializer(model_class):
    class dynamicSeralizer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            exclude = ['lead_id']
    return dynamicSeralizer



def dynamic_serializer_submit(model_class):
    class dynamicSeralizer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'
    return dynamicSeralizer


class assignAssociateSerializer(serializers.ModelSerializer):
    class Meta:
        model = service
        exclude = ['lead_id']





class fieldEmailProposalCountry(serializers.Serializer):
    country = serializers.CharField()

class fieldEmailProposalMarketplace(serializers.Serializer):
    marketplace = serializers.CharField()

class fieldEmailProposalService(serializers.Serializer):
    services = serializers.CharField()

class fieldEmailProposalSlab(serializers.Serializer):
    slab = serializers.CharField()

class fieldaddNewServiceTLSerializer(serializers.Serializer):
    team_leader = serializers.CharField()
    employee_id = serializers.CharField()


class ev_servicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ev_services
        fields = '__all__'


class uploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    class Meta:
        # models=all_identifiers
        fields=["file"]



class getTableFieldsSerializer(serializers.Serializer):
    field = serializers.CharField()
    type = serializers.CharField()
    

class statusUpdateSerializer(serializers.Serializer):
    status = serializers.CharField()


class businessLeadsAllTablesSerializer(serializers.Serializer):
    tables = serializers.ListField()



class serviceFieldSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = service
        fields = '__all__'


class createLeadManualSerializer(serializers.Serializer):
    requester_name = serializers.CharField() 
    phone_number = serializers.CharField() 
    email_id = serializers.EmailField() 
    service_category = serializers.CharField()
    marketplace = serializers.CharField()
    service_country = serializers.CharField()

    def validate(self, attrs):
        requester_name = attrs.get('requester_name')
        phone_number = attrs.get('phone_number')
        email_id = attrs.get('email_id')
        service_category = attrs.get('service_category')
        marketplace = attrs.get('marketplace')
        service_country = attrs.get('service_country')

        print(attrs)

        AI_data = all_identifiers.objects.filter(Q(service_category = service_category) & Q(phone_number = phone_number) | Q(email_id = email_id))

        if AI_data.exists():
            raise serializers.ValidationError('lead already registered with given phone number or email id')
        if service_country is None:
            raise serializers.ValidationError('service_country is required')
        if marketplace is None:
            raise serializers.ValidationError('maketplace is required')
        if service_category is None:
            raise serializers.ValidationError('service category is required')
        if requester_name is None:
            raise serializers.ValidationError('requester name is required')
        if len(phone_number) < 10:
            raise serializers.ValidationError('a valid 10 digit number is required')

        return attrs
    

    def create(self, validated_data):
        lead_id = getLeadId()
        validated_data['lead_id'] = lead_id

        # global service_country_data
        # service_country_data = validated_data['service_country']

        # del validated_data['service_country']

        # print('validated_data', validated_data)

        for key in validated_data:
            if isinstance(validated_data[key] ,str):
                validated_data[key] = validated_data[key].lower()
            else :
                validated_data[key] = validated_data[key]

        data = all_identifiers.objects.create(**validated_data)
        print('data', data.id)
        if data:
            d = {'lead_id': data}

            business_identifiers.objects.create(**d)
            comment.objects.create(**d)
            contact_preference.objects.create(**d)
            seller_address.objects.create(**d)
            followup.objects.create(**d)
            website_store.objects.create(**d)
            d['service_category'] = validated_data['service_category']
            d['service_country'] = validated_data['service_country']
            service.objects.create(**d)

            lead_status_instance = lead_status.objects.get(title = 'yet to contact')
            print('lead_status_instance', lead_status_instance)
            lead_status_record.objects.create(**{'lead_id': data, 'status': lead_status_instance})

        return data
    

class tableFieldSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField(max_length=500, default='')
    type = serializers.CharField()
    dropdown = serializers.CharField()
    dropdown_data = serializers.ListField()

    # class Meta:
    #     extra_kwargs = {'value': {'write_only': True}}
        
        

    # def create(self, validated_data):
    #     print(self)
    #     requester_name = self.validated_data['requester_name']
    #     poc_name = self.validated_data['poc_name']
    #     email_id = self.validated_data['email_id']
    #     service_category = self.validated_data['service_category']
    #     phone_number = self.validated_data['phone_number']

    #     print(requester_name)

        # return super().create(validated_data)




# class fieldAddNewPlatformSerializer(serializers.Serializer):
#     platform = serializers.CharField()

# class fieldAddNewCountrySerializer(serializers.Serializer):
#     service_country = serializers.CharField()

# class fieldAddNewCategorySerializer(serializers.Serializer):
#     service_category = serializers.CharField()

# class fieldAddNewTeamLeaderIdSerializer(serializers.Serializer):
#     team_leader_id = serializers.CharField()
