from graphene_django import DjangoObjectType

from items.models import Item, Category


class ItemType(DjangoObjectType):

    class Meta:
        model = Item
        fields = ('id', 'images', 'title', 'description', 'size', 'color', 'price', 'quantity', 'user', 'category', 'created_at', 'modified_at')


class CategoryType(DjangoObjectType):

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'items')