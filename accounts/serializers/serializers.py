from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from accounts.models import UserProfile

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, label="Password", style={'input_type': 'password'})
    password_2 = serializers.CharField(required=True, label="Confirm Password", style={'input_type': 'password'})
    user_access = serializers.IntegerField(required=False, default=4, min_value=1, max_value=4)
    profile_pic = serializers.ImageField(required=False, default='default.jpg')

    class Meta(object):
        model = User
        fields = ['username', 'password', 'password_2', 'user_access', 'profile_pic']

        extra_kwargs = {
            'password': {'write_only': True},
            'password_2': {'write_only': True}
        }

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value

    def validate_password_2(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):

        user_data = {
            'username': validated_data.get('username'),
            'password': validated_data.get('password'),
            'user_access': validated_data.get('user_access'),
            'profile_pic': validated_data.get('profile_pic')
        }

        user = UserProfile.objects.create_user_profile(
            data=user_data,
            is_active=True,
        )
        validated_data['password'] = None
        validated_data['password_2'] = None
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True, )

    token = serializers.CharField(allow_blank=True, read_only=True)

    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta(object):
        model = User
        fields = ['username', 'password', 'token']

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username:
            raise serializers.ValidationError("Please enter username to login.")

        user = User.objects.filter(Q(username=username)).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            token, created = Token.objects.get_or_create(user=user_obj)
            data['token'] = token
        else:
            raise serializers.ValidationError("User not active.")

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_access', 'date_joined', 'is_active', 'profile_pic', 'is_deleted']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user']
