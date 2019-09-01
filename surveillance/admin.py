from django.contrib import admin
from surveillance.models import State


class StateAdmin(admin.ModelAdmin):
    list_display = ['time', 'liquid_level', 'temperature', 'low_set', 'high_set']
    search_fields = ['time', 'liquid_level', 'temperature', 'low_set', 'high_set']
    list_per_page = 5
    actions_on_top = False
    actions_on_bottom = True


admin.site.register(State, StateAdmin)