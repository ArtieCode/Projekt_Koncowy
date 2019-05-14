from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import AgencyAddress, DetectiveAgency
from tqdm import tqdm
import re


class Command(BaseCommand):
    help = 'Count agencies without a valid address'

    def handle(self, *args, **options):
        all_agencies = DetectiveAgency.objects.all()
        active_count = 0

        def has_active_address(db_object):
            addresses = db_object.agencyaddress_set.all()
            for address in addresses:
                if address.address_type == 2:
                    return True
                return False

        for agency in tqdm(all_agencies):
            has_active = has_active_address(agency)
            if has_active:
                active_count += 1

        print(f'{active_count}/{len(all_agencies)} agencies with an active address')

