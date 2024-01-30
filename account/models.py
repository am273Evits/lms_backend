from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)



class Department(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    def __str__(self): return str(self.title)

class Designation(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    def __str__(self): return str(self.title)

class Product(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    def __str__(self): return str(self.title)

# class Designation(models.Model):
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
#     designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
#     def __str__(self): return str(self.designation)

class Drp_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self): return str(self.department)


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
    employee_id = models.CharField(max_length=100, null=False, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    # user_role = models.ForeignKey(User_role, on_delete=models.CASCADE, null=True, blank=True)
    team_leader = models.ForeignKey("self", related_name = 'team_members' , on_delete=models.CASCADE, null=True, blank=True)
    admin = models.ForeignKey("self", related_name = 'admin_of', on_delete=models.CASCADE, null=True, blank=True)
    # user_links = models.ManyToManyField(user_links)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = True)
    employee_status = models.ForeignKey(Employee_status , on_delete=models.CASCADE, null=True, blank=True)
    # gender = models.ForeignKey(Gender , on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=300, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('self', related_name = 'creator_of', on_delete=models.CASCADE, null=True, blank=True)
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
    

class File(models.Model):
    file = models.FileField(upload_to='files')

class mouFile(models.Model):
    file = models.FileField(upload_to='mou')

class paymentProofFile(models.Model):
    file = models.FileField(upload_to='payment_proof')




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













# from django.db import models
# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser)


# class UserAccountManager(BaseUserManager):
# 	def create_user(self , email , password = None):
# 		if not email or len(email) <= 0 :
# 			raise ValueError("Email field is required !")
# 		if not password :
# 			raise ValueError("Password is must !")
		
# 		user = self.model(
# 			email = self.normalize_email(email) ,
# 		)
# 		user.set_password(password)
# 		user.save(using = self._db)
# 		return user
	
# 	def create_superuser(self , email , password):
# 		user = self.create_user(
# 			email = self.normalize_email(email) ,
# 			password = password
# 		)
# 		user.is_admin = True
# 		user.is_staff = True
# 		user.is_superuser = True
# 		user.save(using = self._db)
# 		return user
	
# class UserAccount(AbstractBaseUser):

#     class gender(models.TextChoices):
#         Male = "Male", "male"
#         Female = "Female", "female"
#     # image=DefaultStaticImageField(upload_to="images",default_image_path='default_img/blank.png',blank=True)
#     email = models.EmailField(max_length = 200 , unique = True)
#     is_active = models.BooleanField(default = True) 
#     is_admin = models.BooleanField(default = False)
#     username = models.CharField(max_length=50, null=False, blank=False)
#     name = models.CharField(max_length=100, null=False)
#     employee_id = models.CharField(max_length=100, null=False, unique=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     employee_status = models.CharField(max_length=300, blank=True, default='')
#     # first_name = models.CharField(max_length=300, blank=True, default='')
#     # name = models.CharField(max_length=300, blank=True, default='')
#     gender = models.CharField(max_length=300, blank=True, default='')
#     date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, default='0001-01-01')
#     blood_group = models.CharField(max_length=300, blank=True, default='')
#     age = models.CharField(max_length=300, blank=True, default='')
#     disability = models.CharField(max_length=300, blank=True, default='')
#     # email_id = models.CharField(max_length=300, blank=True, default='')
#     marital_status = models.CharField(max_length=300, blank=True, default='')
#     mobile_number = models.CharField(max_length=300, blank=True, default='')
#     alternate_mobile_number = models.CharField(max_length=300, blank=True, default='')
#     nationality = models.CharField(max_length=300, blank=True, default='')
#     emergency_contact_number = models.CharField(max_length=300, blank=True, default='')
#     religion = models.CharField(max_length=300, blank=True, default='')

#     visibility = models.BooleanField(default=True)

#     objects = UserAccountManager()

#     USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['username']
    
#     def __str__(self):
#         return self.email
    
#     def has_perm(self, perm, obj=None):
#         return self.is_admin
#     def has_module_perms(self, app_label):
#         return True
    

# class File(models.Model):
#     file = models.FileField(upload_to='files')

# class mouFile(models.Model):
#     file = models.FileField(upload_to='mou')

# class paymentProofFile(models.Model):
#     file = models.FileField(upload_to='payment_proof')


#     USERNAME_FIELD = ["email", 'name', 'employee_id']
    
#     # defining the manager for the UserAccount model
#     objects = UserAccountManager()
    
#     def __str__(self):
#         return str(self.email)
    
#     def has_perm(self , perm, obj = None):
#         return self.is_admin
    
#     def has_module_perms(self , app_label):
#         return True
    
#     def save(self , *args , **kwargs):
#         if not self.type or self.type == None :
#             self.type = UserAccount.Types.TL
#         return super().save(*args , **kwargs)