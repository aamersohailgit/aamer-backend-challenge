import graphene
from django.db import models
from enumfields import EnumField
from enumfields import Enum


class State(Enum):
    NSW = "NSW"
    VIC = "VIC"
    QLD = "QLD"
    SA = "SA"
    WA = "WA"
    TAS = "TAS"
    NT = "NT"
    ACT = "ACT"


class StateEnum(graphene.Enum):
    NSW = "NSW"
    VIC = "VIC"
    QLD = "QLD"
    SA = "SA"
    WA = "WA"
    TAS = "TAS"
    NT = "NT"
    ACT = "ACT"


class Person(models.Model):
    objects = models.Manager()
    email = models.EmailField()
    name = models.CharField(max_length=255)

class Address(models.Model):
    objects = models.Manager()
    number = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=[(tag.value, tag.name) for tag in StateEnum])
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='address')



