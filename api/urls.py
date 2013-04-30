from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import ClientHandler

clients_handler = Resource(ClientHandler)

urlpatterns = patterns(
    '',
    url(r'^clients/$', clients_handler)
)
