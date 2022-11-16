from graphene import relay
from graphene_django import DjangoObjectType

from items.models import Item, Category


class ItemType(DjangoObjectType):

    class Meta:
        model = Item
        fields = ('id', 'images', 'title', 'description', 'size', 'color', 'price', 'quantity', 'user', 'category', 'created_at', 'modified_at')
        description = "Information about all Items posted by customers"
        convert_choices_to_enum = ["color"]


class CategoryType(DjangoObjectType):

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'items')