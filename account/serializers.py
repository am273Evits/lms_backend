from rest_framework import serializers
from .models import *



class loginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=UserAccount
        fields=['email','password']




class AdminRegistrationSerializer(serializers.ModelSerializer):
    # designation = serializers.CharField()
    # department = serializers.CharField()
    # user_role = serializers.CharField(read_only=True)
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    class Meta:
        model = UserAccount
        fields = ['email', 'name', 'employee_id', 'designation', 'department']
        # extra_kwargs = {
        #     'password': {'write_only': True},
        #     'password2': {'write_only': True}
        # }

    def save(self):
        # print(self.validated_data.get('designation'))
  
        if self.validated_data.get('employee_id') == None:
            raise serializers.ValidationError("employee_id field id is required")
        if self.validated_data.get('name') == None:
            raise serializers.ValidationError("name field is required")
        if self.validated_data.get('department') == None:
            raise serializers.ValidationError("department field is required")
        elif not Department.objects.filter(title = self.validated_data.get('department')):
            raise serializers.ValidationError("invalid field department")
        if self.validated_data.get('designation') == None:
            raise serializers.ValidationError("designation is required")
        elif not Designation.objects.filter(title = self.validated_data.get('designation')).exists():
            raise serializers.ValidationError("invalid field designation")
        
        data = self.validated_data
        # print('data', data['designation'])
        # data['designation'] = Designation.objects.filter(title = self.validated_data.get('designation')).first()
        # print('designation',self)

        # self.validated_data['designation'] = 

        user = UserAccount(
            email = self.validated_data['email'],
            name = self.validated_data['name'],
            employee_id = self.validated_data['employee_id'],
            designation = self.validated_data['designation'],
            department = self.validated_data['department'],
            employee_status = Employee_status.objects.get(title = 'active'),
            visibility = True,
        )
        password = 'admin#manager@123'
        # password2 = 'admin#manager@123'
        # if password != password2:
        #     raise serializers.ValidationError('password and return password do not match')
        user.set_password(password)
        user.save()

        return user
    

class LeadManagerRegistrationSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    class Meta:
        model = UserAccount
        fields = ['email', 'name', 'employee_id', 'designation', 'department', 'product']
        # extra_kwargs = {
        #     'password': {'write_only': True},
        #     'password2': {'write_only': True}
        # }

    def save(self):

        print(self.validated_data.get('product'))

        if self.validated_data.get('employee_id') == None:
            raise serializers.ValidationError("employee_id field id is required")
        if self.validated_data.get('name') == None:
            raise serializers.ValidationError("name field is required")
        if self.validated_data.get('department') == None:
            raise serializers.ValidationError("department field is required")
        elif not Department.objects.filter(title = self.validated_data.get('department')):
            raise serializers.ValidationError("invalid field department")
        if self.validated_data.get('designation') == None:
            raise serializers.ValidationError("designation is required")
        elif not Designation.objects.filter(title = self.validated_data.get('designation')).exists():
            raise serializers.ValidationError("invalid field designation")
        if self.validated_data.get('product') == None:
            raise serializers.ValidationError("product is required")
        elif not Product.objects.filter(title = self.validated_data.get('product')).exists():
            raise serializers.ValidationError("invalid field product")


        user = UserAccount(
            email = self.validated_data['email'],
            name = self.validated_data['name'],
            employee_id = self.validated_data['employee_id'],
            designation = self.validated_data['designation'],
            department = self.validated_data['department'],
            product = self.validated_data['product'],
            employee_status = Employee_status.objects.get(title = 'active'),
            visibility = True,
        )
        password = 'evitamin@123'
        # password2 = self.validated_data['password2']
        # if password != password2:
        #     raise serializers.ValidationError('password and return password do not match')
        user.set_password(password)
        user.save()
    
    



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
    product = serializers.CharField()


class viewUserSerializer(serializers.Serializer):
    employee_id = serializers.CharField()
    name = serializers.CharField() 
    designation = serializers.CharField() 
    department = serializers.CharField() 


class viewUserIndividualSerializer(serializers.Serializer):
    employee_id = serializers.CharField() 
    name = serializers.CharField() 
    email_id = serializers.CharField() 
    department = serializers.ListField() 
    designation = serializers.ListField()
    product = serializers.ListField() 
    employee_status = serializers.ListField() 


class updateUserSerializer(serializers.ModelSerializer):
    # name = serializers.CharField()
    # department = serializers.IntegerField()
    # designation = serializers.IntegerField()
    # product = serializers.IntegerField()
    # employee_status = serializers.IntegerField()
    class Meta:
        model = UserAccount
        fields = ['name', 'department', 'designation', 'product', 'employee_status']


class userDeleteSerializer(serializers.ModelSerializer):
    visibility = serializers.BooleanField()
    class Meta:
        model = UserAccount
        fields = ['visibility']

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
