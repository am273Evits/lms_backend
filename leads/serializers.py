from rest_framework import serializers
from .models import *
import re
# from leads.views import resFun
# from dropdown.models import *
# from evitamin.models import *
# from django.db.models import Q
# from rest_framework import status
# from rest_framework.response import Response
# # from rest_framework.exceptions import ValidationError

# from records.models import lead_status_record

from .main_functions import getClientId



# def resFun(status,message,data):
#     res = Response()
#     res.status_code = status
#     res.data = {
#         'status': status,
#         'message': message,
#         'data': data,
#     }
#     return res



class lead_managerBlSerializer_bd(serializers.Serializer):
    id = serializers.CharField()
    client_id = serializers.CharField()
    lead_id = serializers.CharField()
    client_name = serializers.CharField()
    contact_number = serializers.CharField()
    alternate_contact_number = serializers.CharField()
    email_id = serializers.EmailField()
    alternate_email_id = serializers.CharField()
    # service_category = serializers.CharField()
    # assigned_to = serializers.CharField()
    # status = serializers.CharField()
    upload_date = serializers.DateTimeField()
    deadline = serializers.CharField()
    associate = serializers.DictField()
    # service_category = serializers.ListField()
    # commercials = serializers.CharField()
    # status = serializers.CharField()
    client_turnover = serializers.CharField()
    business_name = serializers.CharField()
    business_type = serializers.CharField()
    business_category = serializers.CharField()
    firm_type = serializers.CharField()
    contact_preferences = serializers.CharField()
    # followup = serializers.CharField()
    hot_lead = serializers.BooleanField()
    # country = serializers.CharField()
    # state = serializers.CharField()
    # city = serializers.CharField()
    service = serializers.CharField()
    # associate = serializers.CharField()
    assigned_status = serializers.CharField()
    payment_approval = serializers.CharField()
    mou_approval = serializers.CharField()
    commercial_approval = serializers.DictField()
    commercial = serializers.CharField()
    status = serializers.CharField()
    follow_up = serializers.ListField()



class lead_managerBlSerializer_admin(serializers.Serializer):
    id = serializers.CharField()
    client_id = serializers.CharField()
    client_name = serializers.CharField()
    contact_number = serializers.CharField()
    alternate_contact_number = serializers.CharField()
    email_id = serializers.EmailField()
    alternate_email_id = serializers.CharField()
    # service_category = serializers.CharField()
    # assigned_to = serializers.CharField()
    # status = serializers.CharField()
    upload_date = serializers.DateTimeField()
    deadline = serializers.CharField()
    # associate = serializers.CharField()
    services = serializers.ListField()
    service_category = serializers.ListField()
    # commercials = serializers.CharField()
    # status = serializers.CharField()
    client_turnover = serializers.CharField()
    business_name = serializers.CharField()
    business_type = serializers.CharField()
    business_category = serializers.CharField()
    firm_type = serializers.CharField()
    contact_preferences = serializers.CharField()
    # followup = serializers.CharField()
    hot_lead = serializers.BooleanField()
    request_id = serializers.CharField()
    provider_id = serializers.CharField()
    requester_id = serializers.CharField()
    requester_location = serializers.CharField()
    requester_sell_in_country = serializers.CharField()
    service_requester_type = serializers.CharField()
    lead_owner = serializers.CharField()





# class View_All_Leads(serializers.ModelSerializer):
#     associate = serializers.CharField()
#     service_category = serializers.CharField()
#     commercials = serializers.CharField()
#     status = serializers.CharField()
#     client_turnover = serializers.CharField()
#     business_type = serializers.CharField()
#     business_category = serializers.CharField()
#     firm_type = serializers.CharField()
#     contact_preferences = serializers.CharField()
#     followup = serializers.CharField()
#     country = serializers.CharField()
#     state = serializers.CharField()
#     city = serializers.CharField()
#     # status = serializers.CharField()
#     # associate = serializers.CharField()
#     class Meta:
#         model = Leads
#         exclude = ['visibility', 'email_record', 'created_date', 'current_status']



class CreateCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country']

    def validate(self, data):
        data['country'] = data['country'].lower()
        if not data['country'] or data['country'] == None or data['country'] == '':
            raise serializers.ValidationError('country is a required field')
        return data

    def create(self, validated_data):
        marketplace = Country.objects.create(**validated_data)
        return marketplace
    
class ViewCountrySerializer(serializers.Serializer):
    country = serializers.ListField()

class SearchCountrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    country = serializers.CharField()





class CreateSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ['segment']

    def validate(self, data):
        data['segment'] = data['segment'].lower()

        if not data['segment'] or data['segment'] == None or data['segment'] == '':
            raise serializers.ValidationError('segment is a required field')
        return data

    def create(self, validated_data):
        print('validated_data',validated_data)
        segment = Segment.objects.create(**validated_data)
        return segment
    

class ViewSegmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    # segment = serializers.CharField()
    # visibility = serializers.BooleanField()
    class Meta:
        model = Segment
        fields = '__all__'


class ArchiveSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ['visibility']



class CreateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service']

    def validate(self, data):
        data['service'] = data['service'].lower()

        if not data['service'] or data['service'] == None or data['service'] == '':
            raise serializers.ValidationError('service is a required field')
        return data

    def create(self, validated_data):
        print('validated_data',validated_data)
        service = Service.objects.create(**validated_data)
        return service
    


class ViewServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Service
        fields = '__all__'


class CreateMarketplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = ['marketplace']

    def validate(self, data):
        data['marketplace'] = data['marketplace'].lower()

        if not data['marketplace'] or data['marketplace'] == None or data['marketplace'] == '':
            raise serializers.ValidationError('marketplace is a required field')
        return data

    def create(self, validated_data):
        marketplace = Marketplace.objects.create(**validated_data)
        return marketplace


class MarketplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = '__all__'

    

class CreateProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['program']

    def validate(self, data):
        data['program'] = data['program'].lower()

        if not data['program'] or data['program'] == None or data['program'] == '':
            raise serializers.ValidationError('program is a required field')
        return data

    def create(self, validated_data):
        program = Program.objects.create(**validated_data)
        return program
    

class ProgramSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Program
        fields = '__all__'
    


class CreateSubProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_Program
        fields = ['sub_program']

    def validate(self, data):
        print('data',data)
        data['sub_program'] = data['sub_program'].lower()

        if not data['sub_program'] or data['sub_program'] == None or data['sub_program'] == '':
            raise serializers.ValidationError('sub program is a required field')
        return data

    def create(self, validated_data):
        program = Sub_Program.objects.create(**validated_data)
        return program
    

class SubProgramSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Sub_Program
        fields = '__all__'


class ViewMarketplaceSerializer(serializers.ModelSerializer):
    # marketplace = serializers.ListField()
    id = serializers.IntegerField()
    class Meta:
        model = Marketplace
        fields = '__all__'

class SearchMarketplaceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    marketplace = serializers.CharField()














# class CreateServiceCommercials(serializers.Serializer):
#     pass
    


# class UpdateServicesSerializer(serializers.Serializer):
#     marketplace_id = serializers.IntegerField()
#     service_id = serializers.IntegerField()
#     service_name = serializers.CharField()
#     commercials = serializers.ListField()

#     def validate(self, attrs):
#         instance = self.instance

#         marketplace_id = attrs.get('marketplace_id')
#         service_name = attrs.get('service_name')
#         commercials = attrs.get('commercials')
        
#         for c in commercials:
#             if not isinstance(c.get('price'), int):
#                 raise serializers.ValidationError('price should be a number')
#             if not isinstance(c.get('commission'), int):
#                 raise serializers.ValidationError('commission should be a number')
#             if not c.get('price_for_mou') or c.get('price_for_mou') == None:
#                 raise serializers.ValidationError('price for mou is required field')
            
#         if not service_name or service_name == None or service_name == '':
#             raise serializers.ValidationError('service name is required field')

#         marketplace = Marketplace.objects.filter(id = marketplace_id)
#         if not marketplace.exists():
#             raise serializers.ValidationError('marketplace id is incorrect')
#         return attrs

#     def update(self, instance, validated_data):
#         instance.service_name = validated_data['service_name']
#         instance.save()
#         for c in validated_data['commercials']:
#             if c.get('commercial_id') == None:
#                 del c['commercial_id']
#                 commercial = Commercials.objects.create(**c)
#                 instance.commercials.add(commercial)
#             else:
#                 commercials = Commercials.objects.filter(id = c.get('commercial_id')).first()
#                 commercials.price = c.get('price')
#                 commercials.price_for_mou = c.get('price_for_mou')
#                 commercials.commission = c.get('commission')
#                 commercials.save()
#         return validated_data


#         # for i in instance.commercials.all():
#         #     print(i)

#         # print('********', service)
#         # print('***********************************', instance)
#         # print('&&&&&&&&&&&&&&&&&&&&', validated_data)
#     #     return super().update(instance, validated_data)
    


class ViewServicesSerializer(serializers.Serializer):
    # marketplace_id = serializers.IntegerField()
    # marketplace = serializers.CharField()
    # service = serializers.JSONField()
    service_id = serializers.CharField()
    service_name = serializers.CharField()
    marketplace_id = serializers.CharField()
    marketplace = serializers.CharField()
    # commercial = serializers.ListField()
    # commercial = serializers.ListField()
    # class Meta:
    #     model = Services
    #     fields = ['service_name', 'marketplace']

# class CommercialsSerializer(serializers.ModelSerializer):
#     commercial_id = serializers.IntegerField()
#     commission = serializers.IntegerField()
#     price = serializers.IntegerField()
#     class Meta:
#         model = Commercials
#         fields = '__all__'




    # class Meta:
    #     model = Services
    #     fields = '__all__'





    # def validate (self, attrs):
    #     print('self, attrs', self, attrs)


# class BusinessDevelopmentLeadSerializer(serializers.Serializer):
#     client_id = serializers.CharField() 
#     service_category = serializers.CharField() 
#     associate = serializers.CharField() 
#     lead_status = serializers.CharField()
#     requester_name = serializers.CharField() 
#     phone_number = serializers.CharField() 
#     email_id = serializers.CharField()


# class bd_teamLeaderSerializer(serializers.Serializer):
#     client_id = serializers.CharField()
#     requester_name = serializers.CharField()
#     phone_number = serializers.CharField()
#     email_id = serializers.CharField()
#     service_category = serializers.CharField()
#     associate = serializers.CharField()
#     lead_status = serializers.CharField()



# class allIdentifiersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = all_identifiers
#         fields = '__all__'

# # class businessIdentifiersSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = business_identifiers
# #         exclude = ['client_id']

# # class commentSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = comment
# #         exclude = ['client_id']

# # class contactPreferenceSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = contact_preference
# #         fields = '__all__'

# # class followupSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = followup
# #         exclude = ['client_id']

# # class sellerAddressSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = seller_address
# #         exclude = ['client_id']

# # class serviceSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = service
# #         exclude = ['client_id']

# # class websiteStoreSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = website_store
# #         exclude = ['client_id']



# def dynamic_serializer(model_class):
#     class dynamicSeralizer(serializers.ModelSerializer):
#         # password = serializers.CharField(read_only=True)
#         class Meta:
#             model = model_class
#             exclude = ['client_id']
#     return dynamicSeralizer



# def dynamic_serializer_submit(model_class):
#     class dynamicSeralizer(serializers.ModelSerializer):
#         class Meta:
#             model = model_class
#             fields = '__all__'
#     return dynamicSeralizer


class assignAssociateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_category
        fields = ['associate']





# class fieldEmailProposalCountry(serializers.Serializer):
#     country = serializers.CharField()

# class fieldEmailProposalMarketplace(serializers.Serializer):
#     marketplace = serializers.CharField()

# class fieldEmailProposalService(serializers.Serializer):
#     services = serializers.CharField()

# class fieldEmailProposalSlab(serializers.Serializer):
#     slab = serializers.CharField()

# class fieldaddNewServiceTLSerializer(serializers.Serializer):
#     team_leader = serializers.CharField()
#     employee_id = serializers.CharField()


class ev_servicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_category
        fields = ['pricing']


class uploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    class Meta:
        # models=all_identifiers
        fields=["file"]

class reasonSubmitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    client_id = serializers.IntegerField()
    lead_id = serializers.CharField()


class LeadStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_category
        fields = ['status_history_all']


def serializer_validation(self, attrs, method):
        data = {}

        if attrs.get('client_name'):
            data['client_name'] = attrs.get('client_name')
        if attrs.get('email_id'):
            data['email_id'] = attrs.get('email_id')
        if attrs.get('contact_number'):
            if attrs.get('contact_number') and len(attrs.get('contact_number')) < 9:
                raise serializers.ValidationError('phone number is not valid')
            data['contact_number'] = attrs.get('contact_number')
        if attrs.get('business_name'):
            data['business_name'] = attrs.get('business_name')
        if attrs.get('gst'):
            data['gst'] = attrs.get('gst')
        if attrs.get('seller_address'):
            data['seller_address'] = attrs.get('seller_address')

        if attrs.get('brand_name'):
            data['brand_name'] = attrs.get('brand_name')

        if attrs.get('business_category'):
            if not Business_category.objects.get(id=attrs.get('business_category')):
                raise serializers.ValidationError('business category id is not valid')
            data['business_category'] = Business_category.objects.get(id=attrs.get('business_category'))

        if attrs.get('client_turnover'):
            if not Client_turnover.objects.get(id=attrs.get('client_turnover')):
                raise serializers.ValidationError('business category id is not valid')
            data['client_turnover'] = Client_turnover.objects.get(id=attrs.get('client_turnover'))

        if attrs.get('status') or attrs.get('associate') or attrs.get('service') or attrs.get('marketplace') or attrs.get('program') or attrs.get('sub_program'):

            if not attrs.get('lead_id'):
                raise serializers.ValidationError('lead id is a required field')
            
            if attrs.get('associate'):
                if not drp_lead_status.objects.get(id=attrs.get('status')):
                    raise serializers.ValidationError('status id is not valid')
                data['status'] = drp_lead_status.objects.get(id=attrs.get('status'))

            if method == 'tm':
                if attrs.get('associate'):
                    if not UserAccount.objects.get(id=attrs.get('associate')):
                        raise serializers.ValidationError('associate id is not valid')
                    data['associate'] = UserAccount.objects.get(id=attrs.get('associate'))


            if method == 'admin':
                if attrs.get('service'):

                    if not UserAccount.objects.get(id=attrs.get('segment')):
                        raise serializers.ValidationError('segment id is not valid')

                    if not UserAccount.objects.get(id=attrs.get('service')):
                        raise serializers.ValidationError('service id is not valid')
                    
                    if not UserAccount.objects.get(id=attrs.get('marketplace')):
                        raise serializers.ValidationError('marketplace id is not valid')
                    
                    if not UserAccount.objects.get(id=attrs.get('program')):
                        raise serializers.ValidationError('program id is not valid')
                    
                    if not UserAccount.objects.get(id=attrs.get('sub_program')):
                        raise serializers.ValidationError('sub_program id is not valid')

                    data['associate'] = UserAccount.objects.get(id=attrs.get('associate'))

        return data



class UpdateLeadsSerializer_ADMIN(serializers.ModelSerializer):
    client_name = serializers.CharField(max_length=100)
    email_id = serializers.EmailField()
    contact_number = serializers.CharField(max_length=15)
    business_name = serializers.CharField(max_length=100)
    gst = serializers.CharField(max_length=100)
    seller_address = serializers.CharField(max_length=500)
    brand_name = serializers.CharField(max_length=100)
    business_category = serializers.IntegerField()
    client_turnover = serializers.IntegerField()
    associate = serializers.IntegerField()
    status = serializers.IntegerField()
    segment = serializers.ListField()
    service = serializers.ListField()
    marketplace = serializers.ListField()
    program = serializers.ListField()
    sub_program = serializers.ListField()

    class Meta:
        model = Leads
        fields = ['client_name', 'email_id', 'contact_number', 'business_name', 'gst', 'seller_address', 'business_category', 'client_turnover','associate', 'status', 'brand_name']

    def validate(self, attrs):

        data = serializer_validation(self,attrs, 'admin')
        return data



class UpdateLeadsSerializer_TL(serializers.ModelSerializer):
    client_name = serializers.CharField(max_length=100)
    email_id = serializers.EmailField()
    contact_number = serializers.CharField(max_length=15)
    business_name = serializers.CharField(max_length=100)
    gst = serializers.CharField(max_length=100)
    seller_address = serializers.CharField(max_length=500)
    brand_name = serializers.CharField(max_length=100)
    business_category = serializers.IntegerField()
    client_turnover = serializers.IntegerField()
    associate = serializers.IntegerField()
    status = serializers.IntegerField()
    
    class Meta:
        model = Leads
        fields = ['client_name', 'email_id', 'contact_number', 'business_name', 'gst', 'seller_address', 'business_category', 'client_turnover','associate', 'status', 'brand_name']

    def validate(self, attrs):

        data = serializer_validation(self,attrs, 'tl')

        # data = {}

        # if attrs.get('client_name'):
        #     data['client_name'] = attrs.get('client_name')
        # if attrs.get('email_id'):
        #     data['email_id'] = attrs.get('email_id')
        # if attrs.get('contact_number'):
        #     if attrs.get('contact_number') and len(attrs.get('contact_number')) < 9:
        #         raise serializers.ValidationError('phone number is not valid')
        #     data['contact_number'] = attrs.get('contact_number')
        # if attrs.get('business_name'):
        #     data['business_name'] = attrs.get('business_name')
        # if attrs.get('gst'):
        #     data['gst'] = attrs.get('gst')
        # if attrs.get('seller_address'):
        #     data['seller_address'] = attrs.get('seller_address')

        # if attrs.get('brand_name'):
        #     data['brand_name'] = attrs.get('brand_name')

        # if attrs.get('business_category'):
        #     if not Business_category.objects.get(id=attrs.get('business_category')):
        #         raise serializers.ValidationError('business category id is not valid')
        #     data['business_category'] = Business_category.objects.get(id=attrs.get('business_category'))

        # if attrs.get('client_turnover'):
        #     if not Client_turnover.objects.get(id=attrs.get('client_turnover')):
        #         raise serializers.ValidationError('business category id is not valid')
        #     data['client_turnover'] = Client_turnover.objects.get(id=attrs.get('client_turnover'))

        # if attrs.get('associate'):
        #     if not UserAccount.objects.get(id=attrs.get('associate')):
        #         raise serializers.ValidationError('associate id is not valid')
        #     data['associate'] = UserAccount.objects.get(id=attrs.get('associate'))
        
        # if attrs.get('status'):
        #     if not attrs.get('lead_id'):
        #         raise serializers.ValidationError('service category id is a required field')
        #     if not drp_lead_status.objects.get(id=attrs.get('associate')):
        #         raise serializers.ValidationError('associate id is not valid')
        #     data['associate'] = drp_lead_status.objects.get(id=attrs.get('associate'))
        return data
    

class UpdateLeadsSerializer_TM(serializers.ModelSerializer):
    client_name = serializers.CharField(max_length=100)
    email_id = serializers.EmailField()
    contact_number = serializers.CharField(max_length=15)
    business_name = serializers.CharField(max_length=100)
    gst = serializers.CharField(max_length=100)
    seller_address = serializers.CharField(max_length=500)
    brand_name = serializers.CharField(max_length=100)
    business_category = serializers.IntegerField()
    client_turnover = serializers.IntegerField()
    status = serializers.IntegerField()
    
    class Meta:
        model = Leads
        fields = ['client_name', 'email_id', 'contact_number', 'business_name', 'gst', 'seller_address', 'business_category', 'client_turnover', 'status', 'brand_name']

    def validate(self, attrs):
            
        data = serializer_validation(self, attrs, 'tm')

        # data = {}

        # if attrs.get('client_name'):
        #     data['client_name'] = attrs.get('client_name')
        # if attrs.get('email_id'):
        #     data['email_id'] = attrs.get('email_id')
        # if attrs.get('contact_number'):
        #     if attrs.get('contact_number') and len(attrs.get('contact_number')) < 9:
        #         raise serializers.ValidationError('phone number is not valid')
        #     data['contact_number'] = attrs.get('contact_number')
        # if attrs.get('business_name'):
        #     data['business_name'] = attrs.get('business_name')
        # if attrs.get('gst'):
        #     data['gst'] = attrs.get('gst')
        # if attrs.get('seller_address'):
        #     data['seller_address'] = attrs.get('seller_address')
        # if attrs.get('brand_name'):
        #     data['brand_name'] = attrs.get('brand_name')

        # if attrs.get('business_category'):
        #     if not Business_category.objects.get(id=attrs.get('business_category')):
        #         raise serializers.ValidationError('business category id is not valid')
        #     data['business_category'] = Business_category.objects.get(id=attrs.get('business_category'))

        # if attrs.get('client_turnover'):
        #     if not Client_turnover.objects.get(id=attrs.get('client_turnover')):
        #         raise serializers.ValidationError('business category id is not valid')
        #     data['client_turnover'] = Client_turnover.objects.get(id=attrs.get('client_turnover'))

        
        # if attrs.get('status'):
        #     if not attrs.get('lead_id'):
        #         raise serializers.ValidationError('service category id is a required field')
        #     if not drp_lead_status.objects.get(id=attrs.get('associate')):
        #         raise serializers.ValidationError('associate id is not valid')
            # data['associate'] = drp_lead_status.objects.get(id=attrs.get('associate'))
        return data


    
    # def update(self, instance, validated_data):

        
    #     client_name = validated_data.get('client_name')
    #     email_id = validated_data.get('email_id')
    #     phone_number = validated_data.get('phone_number')
    #     business_name = validated_data.get('business_name')
    #     gst = validated_data.get('gst')
    #     seller_address = validated_data.get('seller_address')
    #     business_category = validated_data.get('business_category')
    #     associate = validated_data.get('associate')
    #     current_status = validated_data.get('current_status')

        # print(instance, validated_data)





# class getTableFieldsSerializer(serializers.Serializer):
#     field = serializers.CharField()
#     type = serializers.CharField()
    

# class statusUpdateSerializer(serializers.Serializer):
#     status = serializers.CharField()


# class businessLeadsAllTablesSerializer(serializers.Serializer):
#     tables = serializers.ListField()



# class serviceFieldSubSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = service
#         fields = '__all__'


class createLeadManualSerializer(serializers.Serializer):
    client_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(max_length = 15, required=True)
    business_name = serializers.CharField(required=True)
    segment = serializers.IntegerField(required=True)
    service = serializers.ListField(required=True)
    marketplace = serializers.ListField(required=True)
    alternate_phone_number = serializers.CharField(required=False)
    email_id = serializers.EmailField(required=False)
    alternate_email_id = serializers.EmailField(required=False)
    brand_name = serializers.CharField(required=False)
    business_category = serializers.IntegerField(required=False)
    client_turnover = serializers.IntegerField(required=False)
    hot_lead = serializers.BooleanField(required=False)

    def validate(self, attrs):
        
        client_name = attrs.get('client_name')
        phone_number = attrs.get('phone_number')
        alternate_phone_number = attrs.get('alternate_phone_number')
        email_id = attrs.get('email_id')
        alternate_email_id = attrs.get('alternate_email_id')
        business_name = attrs.get('business_name')
        brand_name = attrs.get('brand_name')
        business_category = attrs.get('business_category')
        client_turnover = attrs.get('client_turnover')
        hot_lead = attrs.get('hot_lead')
        segment = attrs.get('segment')
        service = attrs.get('service')
        marketplace = attrs.get('marketplace')


        # if business_name is None:
        #     raise serializers.ValidationError('service category is required')
        # if client_name is None:
        #     raise serializers.ValidationError('client name is required')
        # if business_category is None:
        #     raise serializers.ValidationError('business category is required')
        # if client_turnover is None:
        #     raise serializers.ValidationError('client turnover is required')
        # if hot_lead is None:
        #     raise serializers.ValidationError('hot lead is required')
        
        
        duplicate_leads = []
        phone_number_list = [phone_number]
        if alternate_phone_number: phone_number_list.append(alternate_phone_number)
        print(phone_number_list)

        email_id_list = [email_id, alternate_email_id]
        print(email_id_list)

        for ph in phone_number_list:
            if len(ph) < 9:
                raise serializers.ValidationError('a valid digit number is required')
            else:
                dup_contact = Leads.objects.filter(contact_number = ph)
                # dup_contact_list = []
                if dup_contact.exists():
                    for dup in dup_contact:
                        if dup.client_id != None:
                            duplicate_leads.append({'client_id': str(dup.client_id), 'remark': [r.remark for r in dup.remark.all()]})

                            # [str(r.remark) for r in  Remark_history.objects.filter(client_id = dup.id)]
                
        for em in email_id_list:
            pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            input_string = em
            if pattern.match(input_string):
                dup_email = Leads.objects.filter(email_id = em)
                if dup_email.exists():
                    for dup in dup_email:
                        for dcl in duplicate_leads:
                            if str(dcl['client_id']) != str(dup.client_id):
                                print(dcl['client_id'])
                                print(dup.client_id)
                                duplicate_leads.append({'client_id': str(dup.client_id) , 'remarks': [r.remark for r in dup.remark.all()]})
                                break

                                # [str(d.remark) for d in Remark_history.objects.filter(client_id = dup.id)]
                                
            else:
                raise serializers.ValidationError(f'{em} is not a valid email address')

        if duplicate_leads and len(duplicate_leads) > 0:
            # return resFun(status.HTTP_400_BAD_REQUEST, 'lead already exists with this contact number or email id')
            # print('duplicate_leads',duplicate_leads)
            raise serializers.ValidationError('lead already exists with this contact number or email id')
        
        if client_turnover != None:
            client_turnover_INST = Client_turnover.objects.filter(id = client_turnover).exists()
            if not client_turnover_INST:
                raise serializers.ValidationError('client turnover field is not valid')
            
        if business_category != None:
            business_cat_INST = Business_category.objects.filter(id = business_category).exists()
            if not business_cat_INST:
                raise serializers.ValidationError('business category field is not valid')
            
                    
        if not Segment.objects.filter(id = segment).exists():
            raise serializers.ValidationError(f"segment field is not valid")
        

        for sr in service:
            serv_category = Service.objects.filter(id = sr).exists()
            if not serv_category:
                raise serializers.ValidationError(f"service category field is not valid")
            

        for sr in marketplace:
            serv_category = Marketplace.objects.filter(id = sr).exists()
            if not serv_category:
                raise serializers.ValidationError(f"marketplace field is not valid")

        return attrs
    

    def create(self, validated_data):

        print('validated_data', validated_data)

        client_id = getClientId()
        validated_data['client_id'] = client_id


        for key in validated_data:
            if isinstance(validated_data[key] ,str):
                validated_data[key] = validated_data[key].lower()
            else :
                validated_data[key] = validated_data[key]

        # print('validated_data',validated_data)


        v_data = {
            # 'status' : drp_lead_status.objects.filter(title = 'yet to contact').first(), 
            'client_id' : validated_data['client_id'], 
            'client_name': validated_data['client_name'],
            'contact_number': validated_data['phone_number'],
            'email_id': validated_data['email_id'],
            'business_name': validated_data['business_name'], 
            # 'service_category': Services.objects.filter(id = v).first(),
            }
        
        if 'brand_name' in validated_data:
            # 'brand_name': validated_data['brand_name'],
            v_data['brand_name'] = validated_data['brand_name']
        
        if 'alternate_contact_number' in validated_data:
            v_data['alternate_contact_number'] = validated_data['alternate_contact_number']
        if 'alternate_email_id' in validated_data:
            v_data['alternate_email_id'] = validated_data['alternate_email_id']
        if 'business_category' in validated_data:
            v_data['business_category'] = Business_category.objects.filter(id = validated_data['business_category']).first()
        if 'client_turnover' in validated_data:
            v_data['client_turnover'] = Client_turnover.objects.filter(id = validated_data['client_turnover']).first()
        if 'hot_lead' in validated_data:
            v_data['hot_lead'] = validated_data['hot_lead']
            
    
        # 'business_category': Drp_business_category.objects.filter(id = validated_data['business_category']).first(), 
        # 'client_turnover': Client_turnover.objects.filter(id = validated_data['client_turnover']).first(), 
        # 'hot_lead':  validated_data['hot_lead']

        print('v_data',v_data)
    
        data = Leads.objects.create(**v_data)
        print('data', data.id)
        # if data:        


        

        

            # phone_number = [{'contact_number': p, 'client_id': data} for p in validated_data['phone_number']]
            # email_id = [{'email_id': e, 'client_id': data} for e in validated_data['email_id']]
            # service_category = [{'service': Services.objects.filter(id = s).first(), 'client_id': data} for s in validated_data['service_category']]

            # phone_number = [Contact_number.objects.create(**ph) for ph in phone_number]
            # email_id = [email_ids.objects.create(**em) for em in email_id]
            # service_category = [Service_category.objects.create(**sc) for sc in service_category]

            # if phone_number and email_id and service_category:
            #     print('all saved')
            # else :
            #     print('not saved')
        return data
    


class dashboardSerializer(serializers.Serializer):
    lead_status = serializers.ListField()




class AddNewServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_category
        fields = ['lead_id','service']


class CreateFollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followup_history
        exclude = ['created_by']



class AskForDetailEmailSerializer(serializers.Serializer):
    client_id = serializers.CharField()


# class tableFieldSerializer(serializers.Serializer):
#     key = serializers.CharField()
#     value = serializers.CharField(max_length=500, default='')
#     type = serializers.CharField()
#     dropdown = serializers.CharField()
#     dropdown_data = serializers.ListField()


# class leadIdSerializer(serializers.Serializer):
#     client_id = serializers.CharField()


# def visibility_dynamic_serializer(model_class):
#     class visibilitySerializer(serializers.ModelSerializer):
#         class Meta:
#             model = model_class
#             fields = ['visibility']
#     return visibilitySerializer




# class dashboardSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     performance = serializers.ListField()

#     # total_leads = serializers.CharField()
#     # yet_to_contact = serializers.CharField()
#     # converted_leads = serializers.CharField()
#     # follow_up = serializers.CharField()
#     # unresponsive = serializers.CharField()
#     # pending_for_pending = serializers.CharField()
#     # asked_for_details = serializers.CharField()
#     # payment_validation_pending = serializers.CharField()
#     # associate_not_assigned = serializers.CharField()
#     # not_interested = serializers.CharField()

#     # class Meta:
#     #     extra_kwargs = {'value': {'write_only': True}}
        
        

#     # def create(self, validated_data):
#     #     print(self)
#     #     requester_name = self.validated_data['requester_name']
#     #     poc_name = self.validated_data['poc_name']
#     #     email_id = self.validated_data['email_id']
#     #     service_category = self.validated_data['service_category']
#     #     phone_number = self.validated_data['phone_number']

#     #     print(requester_name)

#         # return super().create(validated_data)




# # class fieldAddNewPlatformSerializer(serializers.Serializer):
# #     platform = serializers.CharField()

# # class fieldAddNewCountrySerializer(serializers.Serializer):
# #     service_country = serializers.CharField()

# # class fieldAddNewCategorySerializer(serializers.Serializer):
# #     service_category = serializers.CharField()

# # class fieldAddNewTeamLeaderIdSerializer(serializers.Serializer):
# #     team_leader_id = serializers.CharField()
