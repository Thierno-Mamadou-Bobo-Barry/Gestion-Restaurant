from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, login, password=None, role="TABLE", **extra_fields):
        if not login:
            raise ValueError("Login obligatoire")
        user = self.model(login=login, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(login, password, role="ADMIN", **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("TABLE", "Table"),
        ("SERVEUR", "Serveur"),
        ("CUISINE", "Cuisine"),
        ("ADMIN", "Admin"),
    ]

    login = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    actif = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_active(self):
        return self.actif

    def __str__(self):
        return self.login
