from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import ClientHandler
from api.handlers import PetHandler
from api.handlers import VisitHandler
from api.handlers import ProblemHandler
from api.handlers import ScheduleHandler

clients_handler = Resource(ClientHandler)
pets_handler = Resource(PetHandler)
visits_handler = Resource(VisitHandler)
problems_handler = Resource(ProblemHandler)
schedules_handler = Resource(ScheduleHandler)

urlpatterns = patterns(
    '',
    url(r'^clients/$', clients_handler),
    url(r'^pets/$', pets_handler),
    url(r'^visits/(?P<timestamp>\d+)/$', visits_handler),
    url(r'^visits/$', visits_handler),
    url(r'^problems/$', problems_handler),
    url(r'^schedules/$', schedules_handler)
)
