from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        main_tag_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_main'):
                    main_tag_count += 1
        if main_tag_count > 1:
            raise ValidationError('Можно выбрать только один основной тег.')

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ('title', 'published_at')
    list_filter = ('published_at',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ('name',)

@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ('article', 'tag', 'is_main')
    list_filter = ('is_main',)
    search_fields = ('article__title', 'tag__name')
