from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.tokens import default_token_generator

token_generator = default_token_generator


class UserProfileRegistrationManager(models.Manager):
    @transaction.atomic
    def create_user_profile(self, data, is_active=True):
        password = data.pop('password')
        user = User(**data)
        user.is_active = is_active
        user.set_password(password)
        user.save()

        return user


class UserProfile(models.Model):
    """
    A model for user profile that also stores verification key.
    Any methods under User will reside here.

    """

    ACTIVATED = "ALREADY ACTIVATED"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = UserProfileRegistrationManager()

    class Meta:
        verbose_name = u'user profile'
        verbose_name_plural = u'user profiles'

    def __str__(self):
        return str(self.user)


class User(AbstractUser):
    user_access = models.IntegerField(default=4)
    is_deleted = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.jpg')
    exclude = ('first_name',)

    class Meta:
        db_table = u'Users'
