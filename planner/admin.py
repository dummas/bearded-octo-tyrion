from planner.models import Visit
from planner.models import Problem
from planner.models import Client
from planner.models import Pet
from planner.models import Schedule
from django.contrib import admin


class SchedulesAdmin(admin.ModelAdmin):
    list_display = ('profile', 'start', 'end')


class VisitsAdmin(admin.ModelAdmin):
    list_display = ('from_date', 'to_date')


class ProblemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'color')


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'telephone')


class PetsAdmin(admin.ModelAdmin):
    list_display = ('name', 'client')

admin.site.register(Visit, VisitsAdmin)
admin.site.register(Problem, ProblemsAdmin)
admin.site.register(Client, ClientsAdmin)
admin.site.register(Pet, PetsAdmin)
admin.site.register(Schedule, SchedulesAdmin)
