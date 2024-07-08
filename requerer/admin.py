from django.contrib import admin
from requerer.models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'status', 'impressa', 'analista')
    list_filter = ('impressa', 'deficiencia_tipo')
    prepopulated_fields = {
        'slug': ('cpf',),
    }
