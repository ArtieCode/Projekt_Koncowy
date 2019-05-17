from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import ReferenceCity
from tqdm import tqdm
import copy
import re

import os



class Command(BaseCommand):
    help = 'repair address types'

    def handle(self, *args, **options):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'miejscowosci')
        with open(file_path) as city_file:
            for line in tqdm(city_file):
                city_name = line[0:23]
                city_name = city_name.rstrip()
                city_lon_string = line[24:26] + "." + line[27:29]
                city_lat_string = line[39:41] + "." + line[42:44]
                reference_city = ReferenceCity(city=city_name,
                                               geocoding_latitude=float(city_lat_string),
                                               geocoding_longitude=float(city_lon_string))
                reference_city.save()
