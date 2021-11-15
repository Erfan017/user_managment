from django_filters import rest_framework as filters

from accounts.models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ('username', 'user_access', 'is_deleted')
