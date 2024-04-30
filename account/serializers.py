from rest_framework import serializers
from .models import *
import string
import secrets
from django.contrib.auth.hashers import make_password
from leads.models import *
# from account.views import generate_random_code



def generate_random_code(length=25):
    alphabet = string.ascii_letters + string.digits
    random_code = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_code


class loginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=UserAccount
        fields=['email','password']




def registrationValidation(self):
    if self.validated_data.get('employee_id') == None:
        raise serializers.ValidationError("employee_id field id is required")
    if self.validated_data.get('name') == None:
        raise serializers.ValidationError("name field is required")
    if self.validated_data.get('mobile_number') == None:
        raise serializers.ValidationError("mobile number field is required")

    if len(self.validated_data.get('mobile_number')) > 15 or len(self.validated_data.get('mobile_number')) < 10 :
        raise serializers.ValidationError("mobile number should be of 10 digits")
    if self.validated_data.get('department') == None:
        raise serializers.ValidationError("department field is required")
    elif not Department.objects.filter(id = self.validated_data.get('department')):
        raise serializers.ValidationError("invalid field department")
    if self.validated_data.get('designation') == None:
        pass
        # raise serializers.ValidationError("designation is required")
    elif not Designation.objects.filter(id = self.validated_data.get('designation')).exists():
        raise serializers.ValidationError("invalid field designation")
        # raise serializers.ValidationError("segment is required")
    
    if self.validated_data.get('segment') == None:
        pass
    elif not Segment.objects.filter(id=self.validated_data.get('segment')).exists():
        raise serializers.ValidationError("invalid field segment")
    
    
    if self.validated_data.get('user_manager') == None:
        pass
    elif not UserAccount.objects.filter(id=self.validated_data.get('user_manager')).exists():
        raise serializers.ValidationError("invalid field user manager id")
    
    if self.validated_data.get('lead_manager') == None:
        pass
    elif not UserAccount.objects.filter(id=self.validated_data.get('lead_manager')).exists():
        raise serializers.ValidationError("invalid field lead manager id")
    
    if not UserAccount.objects.filter(id=self.validated_data.get('team_leader')).exists():
        raise serializers.ValidationError("invalid field team manager id")
    
    if not UserAccount.objects.filter(id=self.validated_data.get('director')).exists():
        raise serializers.ValidationError("invalid field director id")
    
    
    if self.validated_data.get('service') == None:
        pass
    elif len(self.validated_data.get('service')) > 0:
        for s in self.validated_data.get('service'):
            if not Service.objects.filter(id=s).exists():
                raise serializers.ValidationError('invalid service id')
    
    if self.validated_data.get('marketplace') == None:
        pass
    elif len(self.validated_data.get('marketplace')) > 0:
        for s in self.validated_data.get('marketplace'):
            if not Marketplace.objects.filter(id=s).exists():
                raise serializers.ValidationError('invalid marketplace id')
            
    if self.validated_data.get('program') == None:
        pass
    elif len(self.validated_data.get('program')) > 0:
        for s in self.validated_data.get('program'):
            if not Program.objects.filter(id=s).exists():
                raise serializers.ValidationError('invalid program id')

    if self.validated_data.get('sub_program') == None:
        pass
    elif len(self.validated_data.get('sub_program')) > 0:
        for s in self.validated_data.get('sub_program'):
            if not Sub_Program.objects.filter(id=s).exists():
                raise serializers.ValidationError('invalid sub_program id')
    


def registrationSave(self):
    user = UserAccount(
        email = self.validated_data['email'].lower(),
        name = self.validated_data['name'].lower(),
        mobile_number = self.validated_data['mobile_number'],
        employee_id = self.validated_data['employee_id'].lower(),
        segment = Segment.objects.get(id=self.validated_data['segment']) if self.validated_data['segment'] != None else self.validated_data['segment'],
        designation = Designation.objects.get(id=self.validated_data['designation']) if self.validated_data['designation'] != None else self.validated_data['designation'],
        department = Department.objects.get(id=self.validated_data['department']),
        user_manager = UserAccount.objects.get(id=self.validated_data['user_manager']) if self.validated_data['user_manager'] != None else self.validated_data['user_manager'],
        lead_manager = UserAccount.objects.get(id=self.validated_data['lead_manager']) if self.validated_data['lead_manager'] != None else self.validated_data['lead_manager'],
        team_leader = UserAccount.objects.get(id=self.validated_data['team_leader']),
        director = UserAccount.objects.get(id=self.validated_data['director']),
        user_pwd_token = generate_random_code(),
        # employee_status = Employee_status.objects.get(title = 'active'),
        visibility = True,
    )
    # password = 'admin#manager@123'
    # user.set_password(password)
    user.save()

    if self.validated_data['service'] and len(self.validated_data['service']) > 0:
        for s in self.validated_data['service']:
            user.service.add(s)

    if self.validated_data['marketplace'] and len(self.validated_data['marketplace']) > 0:
        for s in self.validated_data['marketplace']:
            user.marketplace.add(s)

    if self.validated_data['program'] and len(self.validated_data['program']) > 0:
        for s in self.validated_data['program']:
            user.program.add(s)
    
    if self.validated_data['sub_program'] and len(self.validated_data['sub_program']) > 0:
        for s in self.validated_data['sub_program']:
            user.sub_program.add(s)
    
    return user



class AdminRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    employee_id = serializers.CharField()
    service = serializers.ListField(allow_null=True)
    marketplace = serializers.ListField(allow_null=True)
    program = serializers.ListField(allow_null=True)
    sub_program = serializers.ListField(allow_null=True)
    department = serializers.IntegerField()
    designation = serializers.IntegerField(allow_null=True)
    segment = serializers.IntegerField(allow_null=True)
    user_manager = serializers.IntegerField(allow_null=True)
    lead_manager = serializers.IntegerField(allow_null=True)
    team_leader = serializers.IntegerField()
    director = serializers.IntegerField()
    mobile_number = serializers.CharField()

    class Meta:
        model = UserAccount
        fields = ['email', 'name', 'mobile_number', 'employee_id', 'designation', 'department', 'director', 'user_manager', 'lead_manager', 'team_leader', 'segment', 'service', 'marketplace', 'program', 'sub_program']
        # extra_kwargs = {
        #     'password': {'write_only': True},
        #     'password2': {'write_only': True}
        # }
    def save(self):
        registrationValidation(self)
        user = registrationSave(self)
        return user
 
 

class LeadManagerRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    employee_id = serializers.CharField()
    service = serializers.ListField()
    marketplace = serializers.ListField()
    program = serializers.ListField()
    sub_program = serializers.ListField()
    department = serializers.IntegerField()
    designation = serializers.IntegerField(allow_null=True)
    segment = serializers.IntegerField(allow_null=True)
    user_manager = serializers.IntegerField(allow_null=True)
    lead_manager = serializers.IntegerField(allow_null=True)
    team_leader = serializers.IntegerField()
    director = serializers.IntegerField()
    mobile_number = serializers.CharField()

    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    class Meta:
        model = UserAccount
        fields = ['email', 'name', 'employee_id', 'designation', 'department', 'director', 'user_manager', 'lead_manager', 'team_leader', 'segment', 'service', 'marketplace', 'program', 'sub_program','mobile_number']
        # extra_kwargs = {
        #     'password': {'write_only': True},
        #     'password2': {'write_only': True}
        # }

    def save(self):
        registrationValidation(self)
        user = registrationSave(self)

        return user
    
    



class userSpecificLinkSerializer(serializers.Serializer):
    title = serializers.CharField()
    # link_type = serializers.CharField()
    navigation = serializers.CharField()



class userSerializer(serializers.Serializer):
    # class Meta:
    #     model = UserAccount
    #     fields = ['name', 'email', 'employee_id', 'department', 'designation', 'product']

    email = serializers.CharField()
    name = serializers.CharField()
    employee_id = serializers.CharField()
    department = serializers.CharField()
    designation = serializers.CharField()
    # program = serializers.CharField()


class viewUserSerializer(serializers.Serializer):
    employee_id = serializers.CharField()
    name = serializers.CharField() 
    mobile_number = serializers.CharField()
    email_id = serializers.CharField() 
    designation = serializers.DictField() 
    department = serializers.DictField() 
    # program = serializers.DictField() 
    employee_status = serializers.DictField()
    director = serializers.DictField()
    user_manager = serializers.DictField()
    lead_manager = serializers.DictField()
    team_leader = serializers.DictField()
    segment = serializers.DictField()
    service = serializers.ListField()
    marketplace = serializers.ListField()
    program = serializers.ListField()
    sub_program = serializers.ListField()


# class viewUserIndividualSerializer(serializers.Serializer):
#     employee_id = serializers.CharField() 
#     name = serializers.CharField() 
#     email_id = serializers.CharField() 
#     department = serializers.ListField() 
#     designation = serializers.ListField()
#     product = serializers.ListField() 
#     employee_status = serializers.ListField() 


class updateUserSerializer(serializers.ModelSerializer):
    service = serializers.ListField()
    marketplace = serializers.ListField()
    program = serializers.ListField()
    sub_program = serializers.ListField()
    department = serializers.IntegerField()
    designation = serializers.IntegerField(allow_null=True)
    segment = serializers.IntegerField(allow_null=True)
    user_manager = serializers.IntegerField(allow_null=True)
    lead_manager = serializers.IntegerField(allow_null=True)
    team_leader = serializers.IntegerField()
    director = serializers.IntegerField()
    # name = serializers.CharField()
    # department = serializers.IntegerField()
    # designation = serializers.IntegerField()
    # product = serializers.IntegerField()
    # employee_status = serializers.IntegerField()
    class Meta:
        model = UserAccount
        fields = ['name', 'department', 'designation', 'employee_status', 'service', 'marketplace', 'program', 'sub_program', 'segment', 'user_manager', 'lead_manager', 'team_leader', 'director']

    def validate(self, data):
        if len(dict(data)) == 0:
            raise serializers.ValidationError('data is required to update')
        return data

    def update(self, instance, validated_data):
        print('validated_data',validated_data)
        instance.name = validated_data.get('name')
        # print('validated_data', instance.department ,Department.objects.get(id=validated_data.get('department')) if validated_data.get('department') != None else validated_data.get('department'))
        instance.department = Department.objects.get(id=validated_data.get('department')) if validated_data.get('department') != None else validated_data.get('department')
        instance.designation = Designation.objects.get(id=validated_data.get('designation')) if validated_data.get('designation') != None else validated_data.get('designation')
        instance.employee_status = validated_data.get('employee_status')
        instance.director = UserAccount.objects.get(id=validated_data.get('director')) if validated_data.get('director') != None else validated_data.get('director') 
        instance.segment = Segment.objects.get(id=validated_data.get('segment')) if validated_data.get('segment') != None else validated_data.get('segment')
        instance.user_manager = UserAccount.objects.get(id=validated_data.get('user_manager')) if validated_data.get('user_manager') != None else validated_data.get('user_manager')
        instance.lead_manager = UserAccount.objects.get(id=validated_data.get('lead_manager')) if validated_data.get('lead_manager') != None else validated_data.get('lead_manager')
        instance.team_leader = UserAccount.objects.get(id=validated_data.get('team_leader')) if validated_data.get('team_leader') != None else validated_data.get('team_leader')

        if len(validated_data.get('service')) > 0:
            instance.service.clear()
            for s in validated_data.get('service'):
                instance.service.add(s)

        if len(validated_data.get('marketplace')) > 0:
            instance.marketplace.clear()
            for s in validated_data.get('marketplace'):
                instance.marketplace.add(s)

        if len(validated_data.get('program')) > 0:
            instance.program.clear()
            for s in validated_data.get('program'):
                instance.program.add(s)

        if len(validated_data.get('sub_program')) > 0:
            instance.sub_program.clear()
            for s in validated_data.get('sub_program'):
                instance.sub_program.add(s)



        instance.save()
        return validated_data
    
    # def update(self, validated_data):
    #     return validated_data



class userUnarchiveSerializer(serializers.ModelSerializer):
    visibility = serializers.BooleanField()
    class Meta:
        model = UserAccount
        fields = ['visibility']


class userDeleteSerializer(serializers.ModelSerializer):
    visibility = serializers.BooleanField()
    class Meta:
        model = UserAccount
        fields = ['visibility']


# class userRestoreSerializer(serializers.ModelSerializer):
#     visibility = serializers.BooleanField()
#     class Meta:
#         model = UserAccount
#         fields = ['visibility']

    # def validate(self, attrs):

    #     name = self.get('name')
    #     department = self.get('department')
    #     designation = self.get('designation')
    #     product = self.get('product')
    #     employee_status = self.get('employee_status')


    #     if name is None:
    #         raise serializers.ValidationError('name is required')
        
    #     if department is None:
    #         raise serializers.ValidationError('department is required')
        
    #     if designation is None:
    #         raise serializers.ValidationError('designation is required')
        
    #     if name is None:
    #         raise serializers.ValidationError('name is required')

        # return attrs



    

    # class Meta:
    #     model = UserAccount
    #     fields = ('email', 'name', 'employee_id', 'user_role')
