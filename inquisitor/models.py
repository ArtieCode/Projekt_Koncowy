from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

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


# Raw Registry Data Model - used as local cache of the registry

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


    # Main Agency class - non-sensitive data and settings

class DetectiveAgency(models.Model):

    # Identification

    company_id = models.CharField(max_length=50, primary_key=True)

    # Registry Link:

    registry = models.OneToOneField(to=DetectiveAgencyRecord,
                                       null=True,
                                       blank=True,
                                       on_delete=models.DO_NOTHING)

    # Public Profile - supporting methods for auto fields
    def slugify_company(self):
        return slugify(f"{self.company_id}-{self.company_name}")

    def create_image_path_logo(self):
        return f"{self.company_id}/{self.company_slug}-logo"

    def get_absolute_url(self):
        print('returning slug')
        return f'/{self.company_slug}'

    # Public Profile - data:

    company_name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=300, unique=True)
    logo = models.ImageField(upload_to=create_image_path_logo, null=True)
    description_short = models.CharField(max_length=500, null=True)
    description_long = models.CharField(max_length=5000, null=True)
    main_contact_email = models.CharField(max_length=50, null=True)
    main_telephone_number = models.CharField(max_length=50, null=True)

    # Public Profile - services flags:
    offers_services_marital = models.BooleanField(default=False)
    offers_services_business = models.BooleanField(default=False)
    offers_services_debt = models.BooleanField(default=False)
    offers_services_missing = models.BooleanField(default=False)
    offers_services_observation = models.BooleanField(default=False)
    offers_services_digital = models.BooleanField(default=False)

    # Associated addresses to be accessed via address_set:

    # Management Flags and Tags:

    entity_type = models.IntegerField(choices=ENTITY_TYPES, default=0)
    activated_profile = models.BooleanField(default=False)

    # Default Behaviour Overrides:

    def save(self, *args, **kwargs):
        self.slug = self.slugify_company()
        super(DetectiveAgency, self).save(*args, **kwargs)


class AgencyAddress(models.Model):
    address_type = models.IntegerField(choices=ADDRESS_TYPES)
    owner = models.ForeignKey(to=DetectiveAgency, on_delete=models.CASCADE)
    raw_address = models.CharField(max_length=200, default='')
    street_address = models.CharField(max_length=100, null=True)
    post_code = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=100, null=True)
    voivodship = models.IntegerField(choices=VOIVODSHIP, null=True)
    geocoding_string = models.CharField(max_length=200, null=True)
    geocoding_latitude = models.FloatField(null=True)
    geocoding_longitude = models.FloatField(null=True)







