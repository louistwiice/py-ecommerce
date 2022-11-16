import graphene
import structlog

from django.db.models import Q

from items.models import Item, Category
from serializers.items import ItemType, CategoryType

logger = structlog.get_logger('app-logger')


class CategoryQuery(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    category_children = graphene.List(CategoryType, id=graphene.ID(required=True))
    category_by_id = graphene.Field(CategoryType, id=graphene.ID(required=True))

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_category_children(root, info, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

        return category.get_descendants(include_self=True)

    def resolve_category_by_id(root, info, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

        return category


class ItemQuery(graphene.ObjectType):
    all_items = graphene.List(ItemType)
    item_by_id = graphene.Field(ItemType, id=graphene.ID(required=True, description="Item's ID"))
    items_search = graphene.List(
        ItemType,
        title__icontains=graphene.String(required=False, description="Search items that contains a specific word in title"),
        title__istartswith=graphene.String(required=False, description="Search items that start with a specific word in title")
    )

    user_items = graphene.List(ItemType, id=graphene.ID(description="User's ID"), username=graphene.String(description="User's Username"))

    def resolve_all_items(root, info):

        logger.info('ALL_ITEMS', user=info.context.user.username)
        return Item.objects.all()

    def resolve_item_by_id(root, info, id):
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            return None

        return item

    def resolve_items_search(root, info, title__icontains=None, title__istartswith=None):
        query = Q()

        if title__icontains:
            query = query | Q(title__icontains=title__icontains)

        if title__istartswith:
            query = query | Q(title__istartswith=title__istartswith)

        return Item.objects.filter(query)

    def resolve_user_items(root, info, id=None, username=None):
        """
        Return all items of a specific user
        """

        items = Item.objects.filter(
            Q(user__id=id) | Q(user__username=username)
        )
        return items
