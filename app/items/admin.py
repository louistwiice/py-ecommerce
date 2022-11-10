from django.contrib import admin
from .models import Category, Item
from mptt.admin import DraggableMPTTAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'name')
    list_display_links = ('indented_title', )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'modified_at', 'title', 'quantity', 'price', 'user')
    search_fields = ('id', 'created_at', 'modified_at', 'title', 'user')

