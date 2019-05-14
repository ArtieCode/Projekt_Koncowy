from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import AgencyAddress, DetectiveAgency
from tqdm import tqdm
import re


class Command(BaseCommand):
    help = 'Count agencies without a valid address'

    def handle(self, *args, **options):
        all_agencies = DetectiveAgency.objects.all()
        correct_count = 0

        def validate_address_object(db_object):

            post_code_match = re.match(r'\d{2}-\d{3}', db_object.post_code)
            success = bool(post_code_match)
            return success

        def has_valid_address(db_object):
            addresses = db_object.agencyaddress_set.all()
            valid_count = 0

            for address in addresses:
                validator = validate_address_object(address)
                if validator:
                    valid_count += 1

            if valid_count > 0:
                return True
            else:
                return False

        for agency in tqdm(all_agencies):
            has_valid = has_valid_address(agency)
            if has_valid:
                correct_count += 1

        print(f'{correct_count}/{len(all_agencies)} agencies with a valid address')

