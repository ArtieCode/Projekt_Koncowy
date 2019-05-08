from django.db import models
from django.contrib.auth.models import User

VOIVODSHIP = [
    (2, 'dolnośląskie'),
    (4, 'kujawsko-pomorskie'),
    (6, 'lubelskie'),
    (8, 'lubuskie'),
    (10, 'łódzkie'),
    (12, 'małopolskie'),
    (14, 'mazowieckie'),
    (16, 'opolskie'),
    (18, 'podkarpackie'),
    (20, 'podlaskie'),
    (22, 'pomorskie'),
    (24, 'śląskie'),
    (26, 'świętokrzyskie'),
    (28, 'warmińsko-mazurskie'),
    (30, 'wielkopolskie'),
    (32, 'wielkopolskie'),]
ENTITY_TYPES = [
    (0, "niezdefiniowana"),
    (1, "jednoosobowa działalność gospodarcza"),
    (2, "spółka cywilna"),
    (3, "spółka jawna"),
    (4, "spółka partnerska"),
    (5, "spółka komandytowa"),
    (6, "spółka komandytowo-akcyjna"),
    (7, "spółka z ograniczoną odpowiedzialnością"),
    (8, "spółka akcyjna"),
]
ADDRESS_TYPES = [
    (0, "niezdefiniowany"),
    (1, "adres siedziby"),
    (2, "adres stałego miejsca wykonywania")
]


# Create your models here.
class DetectiveAgencyRecord(models.Model):
    entry_ID = models.CharField(unique=True, max_length=50, primary_key=True)
    entry_date = models.DateField(null=True)
    excision_date = models.DateField(null=True)
    active_status = models.BooleanField()
    firm_name = models.CharField(max_length=250, null=True)
    registered_address = models.CharField(max_length=250, null=True)
    active_addresses = models.CharField(max_length=2000, null=True)
    nip_number = models.CharField(max_length=50, null=True)
    voivodship = models.CharField(max_length=50, null=True)


class DetectiveAgency(models.Model):

    id = models.AutoField(primary_key=True)

    # Registry Data:

    registry_id = models.OneToOneField(DetectiveAgencyRecord, null=True, blank=True)
    registry_entry_date = models.DateField(null=True)
    registry_excision_date = models.DateField(null=True)
    has_active_registration = models.BooleanField(default=False)
    registry_firm_name = models.CharField(max_length=250)
    registry_nip_number = models.CharField(max_length=50, null=True, default=True)

    # Flags and Relations:

    has_associated_account = models.BooleanField(default=False)
    associated_account = models.ForeignKey(to=AgencyAccount, default=None, on_delete=models.PROTECT)
    is_corporation = models.BooleanField(default=False)
    entity_type = models.IntegerField(choices=ENTITY_TYPES, default=0)

class AgencyAddress(models.Model):
    address_type = models.IntegerField(choices=ADDRESS_TYPES)
    owner = models.ForeignKey(to=DetectiveAgency, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    post_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    voivodship = models.IntegerField(choices=VOIVODSHIP, null=True)
    geocoding_string = models.CharField(max_length=200, null=True)
    geocoding_latitude = models.FloatField(null=True)
    geocoding_longitude = models.FloatField(null=True)







