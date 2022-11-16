import graphene
import structlog
import graphql_jwt

from graphene_file_upload.scalars import Upload
from graphql import GraphQLError
from graphql_jwt.decorators import login_required, user_passes_test

from cuser.models import User
from serializers.cuser import UserType
from utilities.common import get_redis_connection, generate_token
from utilities.messages import Mail
from tasks.cuser.auth import task_mail_user

logger = structlog.get_logger('app-logger')


class RegisterMutation(graphene.Mutation):
    """
        Register a new Customer
    """
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
        picture = Upload(required=False)
        phone_number = graphene.String(required=False)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if kwargs.get('password1') != kwargs.get('password2'):
            raise GraphQLError("password1 and password2 don't match")

        password, _ = kwargs.pop('password1'), kwargs.pop('password2')
        email = kwargs.pop('email')
        username = kwargs.pop('username')
        user = User.objects.create_user(
            username=username,
            email=email,
            is_active=False,
            **kwargs
        )
        user.set_password(password)
        user.save()

        red = get_redis_connection()
        otp = generate_token()

        message = Mail.activation(username, otp)
        subject = 'Account activation'
        red.set(f'{username}_otp', otp, ex=5*65)
        task_mail_user.apply_async((subject, [email], message))

        return RegisterMutation(user=user)


class ActivationMutation(graphene.Mutation):
    """
        Activate customer account
    """
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        otp = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        username = kwargs.get('username')
        otp = kwargs.get('otp')
        redis_key = f'{username}_otp'

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise GraphQLError('Username does not exist')

        red = get_redis_connection()
        redis_otp = red.get(redis_key)

        if redis_otp is None:
            raise GraphQLError('OTP expired')

        if redis_otp.decode() == otp:
            user.is_active = True
            user.save()
            red.delete(redis_key)
            return ActivationMutation(user=user)


class ResendOTPMutation(graphene.Mutation):
    """
        Resend activation OTP of a customer
    """

    message = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        redis_key = f'{username}_otp'

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise GraphQLError('Username does not exist')

        red = get_redis_connection()
        otp = generate_token()

        if user.check_password(password):
            message = Mail.activation(user.username, otp)
            subject = 'Resend Account activation'
            red.set(redis_key, otp, ex=5 * 65)
            task_mail_user.apply_async((subject, [user.email], message))

            return ResendOTPMutation(message='OTP resend successfully', user=user)

        raise GraphQLError('Wrong user Password')


class UpdateMutation(graphene.Mutation):
    """
        Update customer account
    """

    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        email = graphene.String(required=False)
        picture = Upload(required=False)
        phone_number = graphene.String(required=False)

    @classmethod
    @login_required
    def mutate(cls, root, info, id, **kwargs):
        user = info.context.user

        if str(user.pk) != str(id) and (user.is_staff is False or user.is_superuser is False):
            raise GraphQLError("Can only perform action in your own user")

        if user.is_active is False:
            raise GraphQLError("User needs to be activated")

        try:
            _ = User.objects.get(id=id)
        except User.DoesNotExist:
            return None

        if 'picture' in kwargs:
            picture = kwargs.pop('picture')
            user.picture = picture
            user.save()

        User.objects.filter(id=id).update(**kwargs)
        user = User.objects.get(id=id)

        return UpdateMutation(user=user)


class ChangePasswordMutation(graphene.Mutation):
    """
        Change user password Account
    """
    message = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        old_password = graphene.String(required=True)
        new_password1 = graphene.String(required=True)
        new_password2 = graphene.String(required=True)

    @classmethod
    @login_required
    @user_passes_test(lambda user: user.is_active)
    def mutate(cls, root, info, **kwargs):
        old_password = kwargs.get('old_password')
        new_password1 = kwargs.get('new_password1')
        new_password2 = kwargs.get('new_password2')

        user = info.context.user
        if not user.check_password(old_password):
            raise GraphQLError("This is not your current password")

        if new_password1 != new_password2:
            raise GraphQLError("New Password 1 and 2 don't match")

        user.set_password(new_password1)
        user.save()
        return ChangePasswordMutation(message='Password successfully changes', user=user)


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_user = RegisterMutation.Field()
    update_user = UpdateMutation.Field()
    activate_user = ActivationMutation.Field()
    resend_otp = ResendOTPMutation.Field()
    change_password = ChangePasswordMutation.Field()
