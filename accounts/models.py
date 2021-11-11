import re
import hashlib
import datetime

from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from django.conf import settings
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator

from base import utils as base_utils
from base import models as base_models

token_generator = default_token_generator

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class UserProfileRegistrationManager(models.Manager):
    """
    Custom manager for ``UserProfile`` model.

    The methods defined here provide shortcuts for user profile creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.

    """

    @transaction.atomic
    def create_user_profile(self, data, is_active=True):
        """
        Create a new user and its associated ``UserProfile``.
        Also, send user account activation (verification) email.

        """

        password = data.pop('password')
        user = User(**data)
        user.is_active = is_active
        user.set_password(password)
        user.save()

        return user

    # def create_profile(self, user):
    #     """
    #     Create UserProfile for give user.
    #     Returns created user profile on success.
    #
    #     """
    #
    #     username = str(getattr(user, User.USERNAME_FIELD))
    #     hash_input = (get_random_string(5) + username).encode('utf-8')
    #     verification_key = hashlib.sha1(hash_input).hexdigest()
    #
    #     profile = self.create(
    #         user=user,
    #         verification_key=verification_key
    #     )
    #
    #     return profile

    def expired(self):
        """
        Returns the list of inactive expired users.

        """

        now = timezone.now() if settings.USE_TZ else datetime.datetime.now()

        return self.exclude(
            models.Q(user__is_active=True) |
            models.Q(verification_key=UserProfile.ACTIVATED)
        ).filter(
            user__date_joined__lt=now - datetime.timedelta(
                getattr(settings, 'VERIFICATION_KEY_EXPIRY_DAYS', 4)
            )
        )

    @transaction.atomic
    def delete_expired_users(self):
        """
        Deletes all instances of inactive expired users.

        """

        for profile in self.expired():
            user = profile.user
            profile.delete()
            user.delete()


class UserProfile(base_models.TimeStampedModel):
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
