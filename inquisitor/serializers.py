from rest_framework import serializers
from inquisitor.models import DetectiveAgency, AgencyAddress


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyAddress
        fields = ('address_type',
                  'street_address',
                  'post_code',
                  'city',
                  'voivodship',
                  'geocoding_latitude',
                  'geocoding_longitude'
                  )

class AgencySerializer(serializers.ModelSerializer):
    agencyaddress_set = AddressSerializer(many=True)

    class Meta:
        model = DetectiveAgency
        fields = ('company_id',
                  'company_name',
                  'slug',
                  'logo',
                  'description_short',
                  'description_long',
                  'main_contact_email',
                  'main_telephone_number',
                  'offers_services_marital',
                  'offers_services_business',
                  'offers_services_debt',
                  'offers_services_missing',
                  'offers_services_observation',
                  'offers_services_digital',
                  'entity_type',
                  'activated_profile',
                  'agencyaddress_set',
                  )