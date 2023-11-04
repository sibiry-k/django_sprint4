from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Describes PostAdmin model."""

    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_display = ('pk',
                    'title',
                    'text',
                    'pub_date',
                    'author',
                    'location',
                    'category',
                    'is_published',
                    'created_at',
                    )
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Location)
