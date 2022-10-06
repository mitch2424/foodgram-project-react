from django.contrib import admin

from .models import Follow, User


class BaseAdminSettings(admin.ModelAdmin):
    """Base admin panel."""
    empty_value_display = '-пусто-'
    list_filter = ('email', 'username')


class UsersAdmin(BaseAdminSettings):
    """Custom admin panel (управление пользователями)."""
    list_display = (
        'id',
        'role',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_display_links = ('id', 'username')
    search_fields = ('role', 'username')


class FollowAdmin(admin.ModelAdmin):
    """Custom admin panel (управление подписками)."""
    list_display = (
        'id',
        'user',
        'author'
    )
    list_display_links = ('id', 'user')
    search_fields = ('user',)


admin.site.register(User, UsersAdmin)
admin.site.register(Follow, FollowAdmin)
