from django.contrib import admin
from requerer.models import Request, Documents


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'status', 'impressa', 'analista')
    list_filter = ('impressa', 'deficiencia_tipo')
    prepopulated_fields = {
        'slug': ('cpf',),
    }
    list_per_page = 10


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'requirement')
    list_display_links = ('id', 'requirement')
    list_per_page = 10
