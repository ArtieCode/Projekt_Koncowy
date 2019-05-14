from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import AgencyAddress
from tqdm import tqdm
import requests
import json
from urllib.parse import urlencode
import types

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
    (32, 'wielkopolskie')]

class Command(BaseCommand):
    help = 'Geocodes addresses in db'

    def handle(self, *args, **options):

        def google_geocode(string):
            url_core = 'https://maps.googleapis.com/maps/api/geocode/json?'

            params = {'address': string,
                      'key': 'AIzaSyD-Voj4JLH8i_eQoiV-UhBiMDXsMjM8hfs'
                      }
            url = url_core + urlencode(params)

            response = requests.get(url)
            parsed_response = json.loads(response.content)
            status = parsed_response['status']
            results = parsed_response['results']
            if len(results) < 1:
                return None
            results = results[0]
            if status != "OK":
                print("something went wrong...")
                return None
            return results


        def geocode_db_address(db_object):
            raw_string = db_object.raw_address

            result = google_geocode(raw_string)

            if result is not None:

                address_components = result['address_components']
                geometry = result['geometry']

                # process geocodes

                location = geometry['location']

                latitude = location['lat']
                longitude = location['lng']


                # set voivodship:
                for entry in address_components:
                    voivodship_present=False
                    types = entry['types']
                    for item in types:
                        if item == 'administrative_area_level_1':
                            voivodship_present = True
                    if voivodship_present:
                        voivodship_code_found = None
                        voivodship_string = entry['short_name']
                        for item in VOIVODSHIP:
                            if voivodship_string == item[1]:
                                voivodship_code_found = item[0]
                        voivodship_code = voivodship_code_found
                        db_object.voivodship = voivodship_code


                # set geocode props:

                db_object.geocoding_latitude = latitude
                db_object.geocoding_longitude = longitude


        addresses_without_geocode = AgencyAddress.objects.filter(geocoding_latitude__isnull=True)

        for address in tqdm(addresses_without_geocode):
            geocode_db_address(address)
            address.save()






