import pytest
import graphene

from cuser.models import User
from schemas.queries.cuser import CUserQuery


@pytest.fixture
def generate_users(mocker):
    return [
        User(id=1, username='John', first_name='Lennon', is_active=True, email='john@mail.com'),
        User(id=2, username='Mike', first_name='Spenser', is_active=True, email='mike@mail.com'),
    ]


@pytest.mark.unitest
class TestCUsers:

    def test_all_users(self, mocker, generate_users):
        mocker.patch.object(
            User.objects,
            'all',
            return_value=generate_users
        )
        query = '''
                     {
                        allUsers {
                            id
                            username
                            isActive
                        }
                     }
                '''

        schema = graphene.Schema(query=CUserQuery)
        result = schema.execute(query)

        assert result.errors is None
        assert 'allUsers' in result.data
        assert len(result.data['allUsers']) == 2

    def test_user_with_no_input_should_return_an_error(self, mocker):
        mocker.patch.object(
            User.objects,
            'get',
            return_value=None
        )

        query = '''
                     {
                        user {
                            id
                            username
                            isActive
                        }
                     }
                '''

        schema = graphene.Schema(query=CUserQuery)
        result = schema.execute(query)

        assert result.errors is not None
        assert result.errors[0].message == 'Either "username" or "id" must be set'

    def test_user_with_id_should_return_object(self, mocker, generate_users):
        mocker.patch.object(
            User.objects,
            'get',
            return_value=generate_users[0]
        )

        query = '''
                     {
                        user(id: 1) {
                            id
                            username
                            isActive
                        }
                     }
                '''

        schema = graphene.Schema(query=CUserQuery)
        result = schema.execute(query)

        assert result.errors is None
        assert result.data['user']['id'] == '1'
        assert result.data['user']['username'] == 'John'

    def test_user_with_username_should_return_object(self, mocker, generate_users):
        mocker.patch.object(
            User.objects,
            'get',
            return_value=generate_users[0]
        )

        query = '''
                     {
                        user(username: "John") {
                            id
                            username
                            isActive
                        }
                     }
                '''

        schema = graphene.Schema(query=CUserQuery)
        result = schema.execute(query)

        assert result.errors is None
        assert result.data['user']['id'] == '1'
        assert result.data['user']['username'] == 'John'

    def test_me_when_not_log_in_should_return_error(self, mocker, generate_users):
        query = '''
                     {
                        me {
                            id
                            username
                            isActive
                        }
                     }
                '''

        schema = graphene.Schema(query=CUserQuery)
        result = schema.execute(query)

        assert result.errors is not None


