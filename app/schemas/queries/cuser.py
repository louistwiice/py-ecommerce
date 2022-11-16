import graphene
import structlog

from cuser.models import User
from graphql import GraphQLError

from serializers.cuser import UserType

logger = structlog.get_logger('app-logger')


class CUserQuery(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, username=graphene.String(required=False, description="Username of the user"), id=graphene.ID(required=False, description="User's ID"))
    me = graphene.Field(UserType)

    def resolve_all_users(root, info):
        print(info.context.user.is_authenticated)
        return User.objects.all()

    def resolve_user(root, info, username=None, id=None):
        if (username, id) == (None, None):
            raise GraphQLError('Either "username" or "id" must be set')

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return None

        return user

    def resolve_me(root, info):
        return info.context.user