from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password):
        if not phone_number:
            raise ValueError('user must have phone number')

        if not email:
            raise ValueError('user must have email')

        if not full_name:
            raise ValueError('user must have full name')

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    #
    def create_customer(self, phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_customer = True
        user.save(using=self._db)
        return user

    #
    def create_operator(self, phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_operator = True
        user.save(using=self._db)
        return user

    def create_nazer(self, phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_nazer = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    roles = [
        ('customer', 'customer'),
        ('nazer', 'nazer'),
        ('operator', 'operator'),
        ('admin', 'admin'),
    ]
    email = models.EmailField(max_length=255, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format: '+919198989'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True, unique=True)
    national_code = models.CharField(max_length=10, null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_nazer = models.BooleanField(default=False)
    is_operator = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    role = models.CharField(choices=roles, max_length=15, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    # def is_customer(self):
    #     return self.is_customer
    #
    # def is_operator(self):
    #     return self.is_operator
    #
    # def is_nazer(self):
    #     return self.is_nazer

    # @is_nazer.setter
    # def is_nazer(self, value):
    #     self._is_nazer = value
    #
    # @is_operator.setter
    # def is_operator(self, value):
    #     self._is_operator = value
    #
    # @is_customer.setter
    # def is_customer(self, value):
    #     self._is_customer = value


class Address(models.Model):
    city_name = models.CharField(max_length=50, null=False)
    avenue_name = models.CharField(max_length=50, null=False)
    street_name = models.CharField(max_length=50, null=False)
    plate = models.CharField(max_length=3, null=False)
    zipCode = models.CharField(max_length=10, null=False)
    customer = models.ForeignKey(User, verbose_name='customer_id', related_name='customer_id',
                                 on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.city_name + ":" + self.avenue_name + ":" + \
               self.zipCode + ":" + self.plate
