from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class CutstomUser(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email,password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using = self._db)
        return user
    

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=25, verbose_name='email', unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)

    objects = CutstomUser()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    
    def has_module_perms(self, ecom_api):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    
class Product(models.Model):
    seller = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    def __str__(self):
        return self.name

class Order(models.Model):
    buyer = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, name='product')
    status =  models.BooleanField(default=False)

    def __str__(self):
        return self.product.name