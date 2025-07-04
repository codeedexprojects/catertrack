from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models

USER_ROLES = (
    ('admin', 'Admin'),
    ('subadmin', 'Subadmin/Captain'),
    ('supervisor', 'Supervisor'),
    ('vice_supervisor', 'Vice Supervisor'),
    ('boys', 'Boys'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, role, password=None, user_name=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if role not in dict(USER_ROLES).keys():
            raise ValueError("Invalid user role")

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, user_name=user_name, **extra_fields)

        if role == 'admin':
            user.is_superuser = True
            user.is_staff = True
        elif role in ['subadmin', 'supervisor', 'vice_supervisor']:
            user.is_staff = True
        else:  
            user.is_staff = False
            user.is_superuser = False

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(
            email=email,
            password=password,
            role='admin',
            user_name='Admin',
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    mobile_number = models.IntegerField(null=True, unique=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"
