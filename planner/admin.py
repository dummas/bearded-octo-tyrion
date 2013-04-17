from planner.models import Visit
from planner.models import Color
from planner.models import Problem
from django.contrib import admin


class VisitsAdmin(admin.ModelAdmin):
    list_display = ('from_date', 'to_date')


class ColorsAdmin(admin.ModelAdmin):
    list_display = ('color_code',)


class ProblemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'color')


admin.site.register(Visit, VisitsAdmin)
admin.site.register(Color, ColorsAdmin)
admin.site.register(Problem, ProblemsAdmin)
