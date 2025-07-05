from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models

USER_ROLES = (
    ('admin', 'Admin'),
    ('subadmin', 'Subadmin/Captain'),
    ('supervisor', 'Supervisor'),
    ('head_boy', 'Head_boy'),
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
    mobile_number = models.CharField(max_length=15,null=True, unique=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"


class StaffDetails(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_details")
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    district = models.CharField(max_length=50)
    place = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  
    profile_image = models.ImageField(upload_to='staff/profile_images/', blank=True, null=True)
    pant = models.BooleanField(default=False)
    shoe = models.BooleanField(default=False)
    grooming = models.BooleanField(default=False)
    experienced = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Staff Details: {self.user.email}"