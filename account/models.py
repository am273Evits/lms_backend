from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)


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
			email = self.normalize_email(email) ,
			password = password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user
	
class UserAccount(AbstractBaseUser):

    class gender(models.TextChoices):
        Male = "Male", "male"
        Female = "Female", "female"
    # image=DefaultStaticImageField(upload_to="images",default_image_path='default_img/blank.png',blank=True)
    email = models.EmailField(max_length = 200 , unique = True)
    is_active = models.BooleanField(default = True) 
    is_admin = models.BooleanField(default = False)
    username = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=100, null=False)
    employee_id = models.CharField(max_length=100, null=False, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    employee_status = models.CharField(max_length=300, blank=True, default='')
    # first_name = models.CharField(max_length=300, blank=True, default='')
    # name = models.CharField(max_length=300, blank=True, default='')
    gender = models.CharField(max_length=300, blank=True, default='')
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, default='0001-01-01')
    blood_group = models.CharField(max_length=300, blank=True, default='')
    age = models.CharField(max_length=300, blank=True, default='')
    disability = models.CharField(max_length=300, blank=True, default='')
    # email_id = models.CharField(max_length=300, blank=True, default='')
    marital_status = models.CharField(max_length=300, blank=True, default='')
    mobile_number = models.CharField(max_length=300, blank=True, default='')
    alternate_mobile_number = models.CharField(max_length=300, blank=True, default='')
    nationality = models.CharField(max_length=300, blank=True, default='')
    emergency_contact_number = models.CharField(max_length=300, blank=True, default='')
    religion = models.CharField(max_length=300, blank=True, default='')

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


    USERNAME_FIELD = ["email", 'name', 'employee_id']
    
    # defining the manager for the UserAccount model
    objects = UserAccountManager()
    
    def __str__(self):
        return str(self.email)
    
    def has_perm(self , perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self , app_label):
        return True
    
    def save(self , *args , **kwargs):
        if not self.type or self.type == None :
            self.type = UserAccount.Types.TL
        return super().save(*args , **kwargs)