from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not username:
#             raise ValueError("Username is required")

#         email = self.normalize_email(email)

#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)        
#         user.save()
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         return self.create_user(username, email, password, **extra_fields)


# class User(AbstractBaseUser, PermissionsMixin):

#     ROLE_CHOICES = (
#         ('user', 'User'),
#         ('moderator', 'Moderator'),
#         ('admin', 'Admin'),
#     )

#     username = models.CharField(max_length=100, unique=True)
#     email = models.EmailField(unique=True)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
#     profile_info = models.TextField(blank=True, null=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = "username"      
#     REQUIRED_FIELDS = ["email"]       

#     def __str__(self):
#         return self.username
