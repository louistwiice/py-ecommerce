import graphene

from graphql_auth.schema import UserQuery, MeQuery

from .mutations.cuser import AuthMutation
from .queries.items import ItemQuery, CategoryQuery
from .queries.cuser import CUserQuery


#class Query(UserQuery, CUserQuery, MeQuery, ItemQuery, CategoryQuery):
class Query(CUserQuery, MeQuery, ItemQuery, CategoryQuery):
    pass


class Mutation(AuthMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

