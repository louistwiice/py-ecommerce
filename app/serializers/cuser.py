from graphene_django import DjangoObjectType
from cuser.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'picture', 'phone_number')
        description = "Information about users"
