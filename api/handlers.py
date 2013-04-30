from piston.handler import BaseHandler
from piston.utils import rc
from planner.models import Client


class ClientHandler(BaseHandler):
    model = Client

    def read(self, request):
        return Client.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data

            client = Client
            try:
                client = Client.objects.get(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    telephone=data['telephone']
                )
                return rc.DUPLICATE_ENTRY
            except client.DoesNotExist:
                client = Client(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    telephone=data['telephone']
                )
                client.save()
                return rc.CREATED
        else:
            super(Client, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            client = Client

            try:
                client = Client.objects.get(
                    id=data['id']
                )
                client.first_name = data['first_name']
                client.last_name = data['last_name']
                client.telephone = data['telephone']
                client.save()
            except client.DoesNotExist:
                return rc.NOT_FOUND
        else:
            super(Client, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTER
