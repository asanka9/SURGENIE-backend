from django.db import models
from hospital.models import Hospital
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, is_admin_staff=None, is_medical_staff=None,role=None, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_admin_staff=is_admin_staff,
            is_medical_staff=is_medical_staff,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    is_scl_content_creator = models.BooleanField(default=False)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    ROLES = [
        ('admin-01', 'Administrator-01'),
        ('admin-02', 'Administrator-02'),
        ('admin-03', 'Administrator-03'),
        ('admin-04', 'Administrator-04'),
        ('admin-05', 'Administrator-05'),
        ('anesthesiologist', 'Anesthesiologist'),
        ('surgeon', 'Surgeon'),
        ('trainee_surgeon', 'Trainee Surgeon'),
        ('nurse', 'Nurse'),
    ]

    is_medical_staff = models.BooleanField(default=False,null=True)
    is_admin_staff = models.BooleanField(default=False,null=True)
    role = models.CharField(max_length=20, choices=ROLES,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)
    telephone = models.CharField(max_length=20)


class Developer(UserProfile):
    role = models.CharField(max_length=50, default='dev')
    # TODO insert user 1:1 relationship


class Surgeon(UserProfile):
    #     first_name = models.CharField(max_length=50)
    #     last_name = models.CharField(max_length=50)
    #     address = models.CharField(max_length=200)
    #     email = models.EmailField(max_length=50)
    specialty = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20)
    # TODO Hospital 1:M relationship
    # TODO User relationship?


class TraineeSurgeon(UserProfile):
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField(max_length=50)
    specialty = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20)
    # TODO experience? hospital? specialty?


class Anesthesiologist(UserProfile):
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField(max_length=50)
    registration_number = models.CharField(max_length=20)
    # TODO user 1:1?
    # TODO Insert hospital 1:M relationship


class Nurse(UserProfile):
    registration_number = models.CharField(max_length=20)
    is_sister = models.BooleanField()  # Sister is the main nurse
    # TODO experience? hospital relationship?


class Admin(UserProfile):
    level = models.IntegerField()
    # TODO insert hospital 1:M relationship
    # TODO user relationship?


class Quote(models.Model):
    quote = models.TextField()

    ROLES = [
        ('admin', 'Administrator'),
        ('surgeon', 'Surgeon'),
        ('trainee_surgeon', 'Trainee Surgeon'),
        ('nurse', 'Nurse')
    ]

    role = models.CharField(max_length=20, choices=ROLES)


class Session(models.Model):
    DAYS = [
        ('sun', 'Sunday'),
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'wednesday'),
        ('thur', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
    ]
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    day = models.CharField(max_length=50, choices=DAYS)


class TraineeSurgeonSession(Session):
    trainee_surgeon = models.ForeignKey(TraineeSurgeon, on_delete=models.CASCADE)
    # TODO trainee surgeon session?


class SurgeonSession(Session):
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    # TODO insert surgeon 1:M relationship
