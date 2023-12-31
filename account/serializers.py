from rest_framework import serializers
from .models import UserAccount



class loginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=UserAccount
        fields=['email','password']




class registrationSerializer(serializers.ModelSerializer):
    designation = serializers.CharField(read_only=True)
    department = serializers.CharField(read_only=True)
    user_role = serializers.CharField(read_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'name', 'employee_id', 'password', 'password2', 'designation', 'department', 'user_role']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }

    def save(self):
        # print('self', self)
        user = UserAccount(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            name = self.validated_data['name'],
            employee_id = self.validated_data['employee_id']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError('password and return password do not match')
        user.set_password(password)
        user.save()

        return user
    



class userSpecificLinkSerializer(serializers.Serializer):
    title = serializers.CharField()
    # link_type = serializers.CharField()
    navigation = serializers.CharField()



class userSerializer(serializers.Serializer):
    email = serializers.CharField()
    name = serializers.CharField()
    employee_id = serializers.CharField()
    user_role = serializers.CharField()
    product = serializers.CharField()

    # class Meta:
    #     model = UserAccount
    #     fields = ('email', 'name', 'employee_id', 'user_role')
