from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)
# from leads.models import Segment



class Department(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    def __str__(self): return str(self.title)

class Designation(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    def __str__(self): return str(self.title)

# class Program_User(models.Model):
#     title = models.CharField(max_length=100, blank=True, default='')
#     def __str__(self): return str(self.title)

# class Sub_Program(models.Model):
#     title = models.CharField(max_length=100, blank=True, default='')
#     def __str__(self): return str(self.title)

# class Designation(models.Model):
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
#     designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
#     def __str__(self): return str(self.designation)

class Drp_Program(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
    # program = models.ForeignKey(Program_User, on_delete=models.CASCADE, null=True, blank=True)
    # sub_program = models.ForeignKey(Sub_Program, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self): return str(self.department)


class canned_email(models.Model):
    email = models.TextField()
    email_type = models.CharField( max_length=50, null=True, blank=True)
    def __str__(self): return str(self.email_type)


# class User_links(models.Model):
#     title = models.CharField(max_length=500, default='', blank=True)
#     link_type = models.CharField(max_length=500, default='', blank=True)
#     user_link = models.CharField(max_length=500, default='', blank=True)
#     access_department = models.CharField(max_length=500, default='', blank=True)
#     table_ref = models.CharField(max_length=500, default='', blank=True)
#     visibility = models.BooleanField(default=False)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
#     designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
#     def __str__(self):
#         return self.title


# class Drp_Product(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
#     designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
#     def __str__(self): return str(self.department)

# class User_role(models.Model):
#     title = models.CharField(max_length=100, blank=True, default='')
#     def __str__(self): return str(self.title)

class Employee_status(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    def __str__(self): return str(self.title)

# class Gender(models.Model):
#     title = models.CharField(max_length=100, blank=True, default='')


class employee_leave_status(models.Model):
    title = models.CharField(max_length=50)


class Employee_leaves(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    notes = models.CharField(max_length=300)
    status = models.ForeignKey(employee_leave_status, on_delete=models.CASCADE)
    employee = models.ForeignKey("account.useraccount", related_name='employee_leave' ,on_delete=models.CASCADE)



class UserAccountManager(BaseUserManager):
	def create_user(self , email , password = None):
		if not email or len(email) <= 0 :
			raise ValueError("Email field is required !")
		if not password :
			raise ValueError("Password is must !")
		
		user = self.model(
			email = self.normalize_email(email) ,
		)
		user.set_password(password)
		user.save(using = self._db)
		return user
	
	def create_superuser(self , email , password):
		user = self.create_user(
			email = self.normalize_email(email),
			password = password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user
      

class UserAccount(AbstractBaseUser):
    email = models.EmailField(max_length = 200 , unique = True)
    name = models.CharField(max_length=100, null=False)
    # username = models.CharField(max_length=50)(max_length = 200, unique = True)
    # contact_number = models.CharField(max_length=15, null=False, blank=True)
    employee_id = models.CharField(max_length=100, null=False, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
    # program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    # user_role = models.ForeignKey(User_role, on_delete=models.CASCADE, null=True, blank=True)
    # admin = models.ForeignKey("self", related_name = 'admin_of', on_delete=models.CASCADE, null=True, blank=True)
    # user_links = models.ManyToManyField(user_links)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = True)
    # employee_status = models.BooleanField(default = True)
    employee_status = models.ForeignKey(Employee_status , on_delete=models.CASCADE, default=1)
    director = models.ForeignKey('self', related_name = 'director_of', on_delete=models.CASCADE, null=True, blank=True)
    user_manager = models.ForeignKey('self', related_name = 'user_manager_of', on_delete=models.CASCADE, null=True, blank=True)
    lead_manager = models.ForeignKey('self', related_name = 'lead_manager_of', on_delete=models.CASCADE, null=True, blank=True)
    team_leader = models.ForeignKey("self", related_name = 'team_leaders_of' , on_delete=models.CASCADE, null=True, blank=True)
    segment = models.ForeignKey("leads.Segment", on_delete=models.CASCADE, null=True, blank=True)
    service = models.ManyToManyField("leads.Service")
    marketplace = models.ManyToManyField("leads.Marketplace")
    program = models.ManyToManyField("leads.Program")
    sub_program = models.ManyToManyField("leads.Sub_program")
    # service = models.ManyToManyField(Service)
    # gender = models.ForeignKey(Gender , on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('self', related_name = 'creator_of', on_delete=models.CASCADE, null=True, blank=True)
    user_pwd_token = models.CharField(max_length=300, blank=True, default='')
    employee_leaves = models.ManyToManyField(Employee_leaves, related_name='user_accounts')
    visibility = models.BooleanField(default=True)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True




class user_delete(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    def __str__(self): return str(self.user.name)

class user_restore(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    def __str__(self): return str(self.user.name)


# class File(models.Model):
#     file = models.FileField(upload_to='files')






    # USERNAME_FIELD = ["email", 'name', 'employee_id']
    
    # # defining the manager for the UserAccount model
    # objects = UserAccountManager()
    
    # def __str__(self):
    #     return str(self.email)
    
    # def has_perm(self , perm, obj = None):
    #     return self.is_admin
    
    # def has_module_perms(self , app_label):
    #     return True
    
    # def save(self , *args , **kwargs):
    #     if not self.type or self.type == None :
    #         self.type = UserAccount.Types.TL
    #     return super().save(*args , **kwargs)