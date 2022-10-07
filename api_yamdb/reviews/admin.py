from django.contrib import admin

from reviews.models import Comment, Review, Genre, Category, Title


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс, формирующий админ-панель сайта, раздел: жанры."""
    list_display = (
        'name', 'slug',
    )
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class GenreAdmin(admin.ModelAdmin):
    """Класс, формирующий админ-панель сайта, раздел: категории."""
    list_display = (
        'name', 'slug',
    )
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс, формирующий админ-панель сайта, раздел: Произведения."""
    list_display = (
        'name', 'year', 'description',
        'category', 'genre'
    )
    filter_horizontal = ('genre',)
    search_fields = ('name', 'year',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'

    def genre(self, obj):
        return obj.mtm_field.through.genre


class ReviewAdmin(admin.ModelAdmin):
    """Класс, формирующий админ-панель сайта, раздел: отзывы."""
    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """Класс, формирующий админ-панель сайта, раздел: комментарии."""
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)

admin.site.register(Comment, CommentAdmin)
