import pytest
import redis
import graphene

from unittest.mock import patch
from model_bakery import baker

from cuser.models import User
from schemas.mutations.cuser import AuthMutation


@pytest.fixture(scope="module")
def mock_redis_set():
    """
        Use to mock redis .set function
    """
    with patch.object(redis, 'Redis', autospec=True) as m:
        m.set.return_value = True
        yield m


@pytest.mark.unitest
class TestAuthMutation:

    @pytest.mark.parametrize('query,variables', [
        ('''
            mutation($firstName: String!, $lastName: String!, $password1: String!, $password2: String!) {
                    createUser(firstName: $firstName, lastName: $lastName, password1: $password1, password2: $password2) {
                    user {
                        id
                        username
                        firstName
                        lastName
                        email
                        isActive
                    }
                }
            }
        ''', {
            'firstName': 'user_mike',
            'lastName': 'user_moke_last_name',
            'password1': 'somepassword1',
            'password2': 'some_other_password2',
        }),
        ('''
            mutation($email: String!, $firstName: String!, $lastName: String!, $password1: String!, $password2: String!) {
                    createUser(email: $email ,firstName: $firstName, lastName: $lastName, password1: $password1, password2: $password2) {
                    user {
                        id
                        username
                        firstName
                        lastName
                        email
                        isActive
                    }
                }
            }
        ''', {
            'firstName': 'user_mike',
            'email': 'email@mail.com',
            'lastName': 'user_moke_last_name',
            'password1': 'somepassword1',
            'password2': 'some_other_password2',
        })
    ])
    def test_create_user_when_forgot_username_email_should_not_passed(self, query, variables):

        schema = graphene.Schema(mutation=AuthMutation)
        result = schema.execute(query, variable_values=variables)

        assert result.errors is not None

    @pytest.mark.django_db
    def test_create_user_with_wrong_password_should_not_passed(self, mocker):
        user = baker.make('cuser.User', _quantity=1, is_active=False)[0]
        query = '''
                    mutation($username: String!, $firstName: String!, $lastName: String!, $email: String!, $password1: String!, $password2: String!) {
                            createUser(username: $username, firstName: $firstName, lastName: $lastName, email: $email, password1: $password1, password2: $password2) {
                            user {
                                id
                                username
                                firstName
                                lastName
                                email
                                isActive
                            }
                        }
                    }
                '''

        variables = {
            'username': user.username,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'password1': 'somepassword1',
            'password2': 'some_other_password2',
        }

        schema = graphene.Schema(mutation=AuthMutation)
        result = schema.execute(query, variable_values=variables)

        assert result.errors is not None
        assert result.errors[0].message == "password1 and password2 don't match"

    @pytest.mark.django_db
    def test_create_user_should_pass(self, mocker, mock_redis_set):
        user = baker.make('cuser.User', _quantity=1, is_active=False)[0]
        mocker.patch('schemas.mutations.cuser.generate_token', return_value=0000)

        mocker.patch.object(
            User.objects,
            'create_user',
            return_value=user
        )

        mocker.patch('schemas.mutations.cuser.Mail.activation', return_value="Activation message is sent")
        mocker.patch('schemas.mutations.cuser.task_mail_user.apply_async', return_value=None)

        query = '''
            mutation($username: String!, $email: String!, $firstName: String!, $lastName: String!, $password1: String!, $password2: String!) {
                    createUser(username: $username, email: $email ,firstName: $firstName, lastName: $lastName, password1: $password1, password2: $password2) {
                    user {
                        id
                        username
                        firstName
                        lastName
                        email
                        isActive
                    }
                }
            }
        '''

        variables = {
            'username': user.username,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'password1': 'somepassword1',
            'password2': 'somepassword1',
        }

        schema = graphene.Schema(mutation=AuthMutation)
        result = schema.execute(query, variable_values=variables)

        assert result.errors is None
        assert 'createUser' in result.data
        assert 'user' in result.data['createUser']

        created_user = result.data['createUser']['user']
        assert created_user['username'] == user.username
        assert created_user['firstName'] == user.first_name
