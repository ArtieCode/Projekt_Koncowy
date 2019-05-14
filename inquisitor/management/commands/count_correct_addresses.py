from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import AgencyAddress
from tqdm import tqdm
import re


class Command(BaseCommand):
    help = 'Processes Google-formatted address strings into model fields'

    def handle(self, *args, **options):
        def validate_address_string(db_object):

            post_code_match = re.match(r'\d{2}-\d{3}', db_object.post_code)
            success = bool(post_code_match)
            return success


        all_addresses = AgencyAddress.objects.all()
        correct_count = 0

        for address in tqdm(all_addresses):

            correct_record = validate_address_string(address)
            if correct_record:
                correct_count += 1
            else:
                address.street_address = ''
                address.post_code = ''
                address.city = ''
                address.save()
        print(f'{correct_count} correct addresses')

