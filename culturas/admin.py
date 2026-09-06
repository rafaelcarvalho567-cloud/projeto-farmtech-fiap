from django.contrib import admin
from .models import Cultura


@admin.register(Cultura)
class CulturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'largura', 'comprimento', 'area', 'ruas', 'criado_em')
    search_fields = ('nome',)
