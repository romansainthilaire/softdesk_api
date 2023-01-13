from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# https://docs.djangoproject.com/en/4.1/topics/auth/customizing


class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email)
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
            )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Project(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.title
