from rest_framework import serializers
from .models import *
from dropdown.models import *
from evitamin.models import *


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
        models=all_identifiers
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


# class fieldAddNewPlatformSerializer(serializers.Serializer):
#     platform = serializers.CharField()

# class fieldAddNewCountrySerializer(serializers.Serializer):
#     service_country = serializers.CharField()

# class fieldAddNewCategorySerializer(serializers.Serializer):
#     service_category = serializers.CharField()

# class fieldAddNewTeamLeaderIdSerializer(serializers.Serializer):
#     team_leader_id = serializers.CharField()
