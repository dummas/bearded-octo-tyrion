from django.contrib.auth.models import User
from piston.handler import BaseHandler
from piston.utils import rc
from planner.models import Client
from planner.models import Pet
from planner.models import Visit
from planner.models import Problem
from planner.models import Schedule


class ScheduleHandler(BaseHandler):
    model = Schedule

    def read(self, request):
        return Schedule.objects.works_today()

    def create(self, request):
        return rc.NOT_IMPLEMENTER

    def update(self, request):
        return rc.NOT_IMPLEMENTER

    def delete(self, request):
        return rc.NOT_IMPLEMENTER


class ProblemHandler(BaseHandler):
    model = Problem

    def read(self, request):
        return Problem.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data
            problem = Problem(
                name=data['name'],
                code=data['code'],
                color=data['color']
            )
            problem.save()
            return rc.CREATED
        else:
            super(Problem, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data
            problem = Problem

            try:
                problem = Problem.objects.get(id=data['id'])
            except problem.DoesNotExist:
                return rc.NOT_FOUND

            problem.name = data['name']
            problem.code = data['code']
            problem.color = data['color']

            problem.save()

            return rc.ALL_OK
        else:
            super(Problem, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTER


class PetHandler(BaseHandler):
    model = Pet

    def read(self, request):
        return Pet.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data

            pet = Pet(
                name=data['name'],
                client=Client.objects.get(id=data['client'])
            )
            pet.save()
            return rc.CREATED
        else:
            super(Pet, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data
            pet = Pet

            try:
                pet = Pet.objects.get(id=data['id'])
            except pet.DoesNotExist:
                return rc.NOT_FOUND

            pet.name = data['name']
            pet.client = Client.objects.get(id=data['client'])

            pet.save()
            return rc.ALL_OK
        else:
            super(Pet, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTER


class VisitHandler(BaseHandler):
    model = Visit

    def read(self, request, timestamp=None):
        if timestamp:
            return Visit.objects.on_that_day(timestamp)
        else:
            return Visit.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data

            visit = Visit(
                from_date=data['from_date'],
                to_date=data['to_date'],
                problem=Problem.objects.get(id=data['problem']),
                description=data['description'],
                client=Client.objects.get(id=data['client']),
                pet=Pet.objects.get(id=data['pet']),
                appointment_to=User.objects.get(id=data['appointment_to']),
                appointment_by=User.objects.get(id=data['appointment_by'])
            )
            visit.save()
            return rc.CREATED
        else:
            super(Visit, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            visit = Visit

            try:
                visit = Visit.objects.get(id=data['id'])
            except visit.DoesNotExist:
                return rc.NOT_FOUND

            visit.from_date = data['from_date']
            visit.to_date = data['to_date']
            visit.problem = Problem.objects.get(id=data['problem'])
            visit.description = data['description']
            visit.client = Client.objects.get(id=data['client'])
            visit.pet = Pet.objects.get(id=data['pet'])
            visit.appointment_to = User.objects.get(
                id=data['appointment_to'])
            visit.appointment_by = User.objects.get(
                id=data['appointment_by'])

            visit.save()

            return rc.ALL_OK
        else:
            super(Visit, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTER


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
                return rc.ALL_OK
            except client.DoesNotExist:
                return rc.NOT_FOUND
        else:
            super(Client, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTER
