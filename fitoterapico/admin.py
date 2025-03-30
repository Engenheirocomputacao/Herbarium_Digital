from django.contrib import admin
from .models import Fitoterapico, Tipo

class TipoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

    
class FitoterapicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'descricao' , 'propriedades', 'indicacao', 'preco')
    search_fields = ('nome', 'especie', 'descricao', 'propriedades', 'indicacao')





admin.site.register(Tipo, TipoAdmin)
admin.site.register(Fitoterapico, FitoterapicoAdmin)    