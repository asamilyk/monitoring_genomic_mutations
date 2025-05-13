from django.contrib import admin
from django.utils.html import format_html
from .models import FilterHistory

@admin.register(FilterHistory)
class FilterHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'filter_name', 'created_at', 'filter_description', 'actions_buttons')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'filter_name', 'filter_params')
    date_hierarchy = 'created_at'
    readonly_fields = ('user', 'created_at', 'filter_params', 'filter_params_formatted')
    fieldsets = (
        (None, {
            'fields': ('user', 'filter_name', 'created_at')
        }),
        ('Параметры фильтра', {
            'fields': ('filter_params_formatted',),
            'classes': ('collapse',)
        }),
        ('Сырые данные', {
            'fields': ('filter_params',),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        url = f"/admin/auth/user/{obj.user.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'Пользователь'
    
    def filter_description(self, obj):
        desc = obj.get_filter_description()
        if len(desc) > 100:
            return f"{desc[:100]}..."
        return desc
    filter_description.short_description = 'Описание фильтра'
    
    def filter_params_formatted(self, obj):
        import json
        from django.utils.safestring import mark_safe
        try:
            params = json.loads(obj.filter_params)
            formatted_json = json.dumps(params, indent=4, ensure_ascii=False)
            return mark_safe(f'<pre>{formatted_json}</pre>')
        except json.JSONDecodeError:
            return "Недействительный JSON"
    filter_params_formatted.short_description = 'Параметры фильтра (форматированный JSON)'
    
    def actions_buttons(self, obj):
        from django.urls import reverse
        apply_url = obj.get_filter_url()
        return format_html(
            '<a class="button" href="{}" target="_blank">Применить</a>',
            apply_url
        )
    actions_buttons.short_description = 'Действия'
