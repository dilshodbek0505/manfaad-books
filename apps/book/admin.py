from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings

from apps.book.models import Book, Author, Category, UserBookRating, BookChapter, Goal, \
    Collection, UserStatistics, Story, StoryUser
from apps.book.api_endpoints.UserStatistics.forms import UserStatisticsForm


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category_name", "like_count")
    list_filter = ("category", "author", "author")

    @admin.display()
    def category_name(self, obj):
        return format_html(f'<div style="display: flex; align-items: center; gap: 10px;"><img src="{obj.category.icon.url}" width="20"  height="20" alt="{obj.category.name}">{obj.category.name}</div>')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("full_name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name",)

    @admin.display()
    def category_name(self, obj):
        return format_html(f'<div style="display: flex; align-items: center; gap: 10px;"><img src="{obj.icon.url}" width="20"  height="20" alt="{obj.name}">{obj.name}</div>')


@admin.register(UserBookRating)
class UserBookRatingAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "is_liked")


@admin.register(BookChapter)
class BookChapterAdmin(admin.ModelAdmin):
    list_display = ("book", "title", "seconds")

    @admin.display()
    def seconds(self, obj):
        icon_url = f'{settings.MEDIA_URL}duration_icon.png'
        return format_html(f'<div style="display: flex; align-items: center; gap: 10px;"><img src="{icon_url}" width="20"  height="20" alt="duration">{obj.point.total_seconds()} s</div>')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("name", "categories_count")

    @admin.display()
    def categories_count(self, obj):
        data = str()
        for category in obj.categories.all():
            icon_url = category.icon.url
            data += f'<div style="display: flex; align-items: center; gap: 10px;"><img src="{icon_url}" width="20"  height="20" alt="{category.name}"><b>{category.name}</b></div>'

        return format_html(data)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "banner")

    @admin.display()
    def banner(self, obj):
        context_html = f"<img src='{obj.image.url}' width='100'  height='100' alt='{obj.name}'>"
        return format_html(context_html)


@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    list_display = ("user__full_name",)
    form = UserStatisticsForm


admin.site.register(Story)
admin.site.register(StoryUser)