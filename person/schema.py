import graphene
from django.shortcuts import get_object_or_404
from enumfields import EnumField
from graphene_django.types import DjangoObjectType

from person.models import Address, Person, State, StateEnum


# state Enum
# class StateEnum(graphene.Enum):
#     NSW = "NSW"
#     VIC = "VIC"
#     QLD = "QLD"
#     SA = "SA"
#     WA = "WA"
#     TAS = "TAS"
#     NT = "NT"
#     ACT = "ACT"


class AddressType(DjangoObjectType):
    class Meta:
        model = Address

    state = EnumField(State)


class PersonType(DjangoObjectType):
    class Meta:
        model = Person


# Get
class PersonQuery(graphene.ObjectType):
    all_people = graphene.List(PersonType)
    all_addresses = graphene.List(AddressType)
    person = graphene.Field(PersonType, id=graphene.Int())

    def resolve_all_people(self, info, **kwargs):
        return Person.objects.all()

    def resolve_all_addresses(self, info, **kwargs):
        return Address.objects.all()

    def resolve_address(self, info, **kwargs):
        id = kwargs.get('id')
        if id:
            try:
                return Address.objects.get(pk=id)
            except:
                return Exception("Address with id {} does not found.".format(id))

    def resolve_person(self, info, **kwargs):
        id = kwargs.get('id')
        if id:
            try:
                return Person.objects.get(pk=id)
            except:
                return Exception("Person with id {} does not found.".format(id))


# Create
class CreatePerson(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        number = graphene.Int(required=True)
        street = graphene.String(required=True)
        city = graphene.String(required=True)
        state = StateEnum(required=True)

    person = graphene.Field(lambda: PersonType)

    def mutate(self, info, email, name, number, street, city, state):

        person = Person.objects.create(
            email=email,
            name=name,
        )

        address = Address.objects.create(
            number=number,
            street=street,
            city=city,
            state=state.value,
            person=person
        )
        return CreatePerson(person=person)


# class UpdatePerson(graphene.Mutation):
#     class Arguments:
#         id = graphene.Int(required=True)
#         email = graphene.String()
#         name = graphene.String()
#         number = graphene.Int()
#         street = graphene.String()
#         city = graphene.String()
#         state = StateEnum()
#     person = graphene.Field(lambda: PersonType)
#
#     def mutate(self, info, id, email=None, name=None, number=None, street=None, city=None, state=None):
#         try:
#             person = Person.objects.get(pk=id)
#         except Person.DoesNotExist:
#             return Exception("Person with id {} does not exist.".format(id))
#         if email:
#             person.email = email
#         if name:
#             person.name = name
#         person.save()
#         address = person.address
#         if number:
#             address.number = number
#         if street:
#             address.street = street
#         if city:
#             address.city = city
#         if state:
#             address.state = state.value
#         address.save()
#         return UpdatePerson(person=person)

# Delete
class UpdatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        email = graphene.String()
        name = graphene.String()
        number = graphene.Int()
        street = graphene.String()
        city = graphene.String()
        state = StateEnum()
        address_id = graphene.Int()

    person = graphene.Field(lambda: PersonType)

    def mutate(self, info, id, email=None, name=None, address_id=None, number=None, street=None, city=None, state=None):
        try:
            person = Person.objects.get(pk=id)
        except Person.DoesNotExist:
            return Exception("Person with id {} does not found.".format(id))
        if name:
            person.name = name
        if email:
            person.email = email
        try:
            address = Address.objects.get(pk=address_id)
            address.number = number
            address.street = street
            address.city = city
            if state in [tag.name for tag in StateEnum]:
                address.state = state.value
            else:
                raise ValueError("Invalid state value")
            address.save()
        except Address.DoesNotExist:
            return Exception("Address with id {} does not found.".format(id))
        person.save()
        return UpdatePerson(person=person)

class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            person = Person.objects.get(pk=id)
            person.delete()
            success = True
        except Person.DoesNotExist:
            return Exception("Person with provided addressId {} not found".format(id))
        return DeletePerson(success=success)


class Mutations(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    delete_person = DeletePerson.Field()


person_schema = graphene.Schema(query=PersonQuery, mutation=Mutations)
