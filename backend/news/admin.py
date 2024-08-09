from django.contrib import admin
from django.utils.safestring import mark_safe

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'created_at',)
    search_fields = ('title', 'description')

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="auto" />')
        return "No Image"

    image_tag.short_description = 'Изображение'
