from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import AgencyAddress, DetectiveAgency
from tqdm import tqdm
import copy
import re


class Command(BaseCommand):
    help = 'repair address types'

    def handle(self, *args, **options):
        all_agencies = DetectiveAgency.objects.all()
        repair_count = 0

        def repair_address(db_object):
            addresses = db_object.agencyaddress_set.all()

            if addresses is not None:

                registered_count = 0
                active_count = 0

                for address in addresses:
                    address_type = address.address_type
                    if address_type == 1:
                        registered_count += 1
                    if address_type == 2:
                        active_count += 1

                    if active_count == 2:
                        address.address_type = 1
                        address.save()
                        return True

            return False

        for agency in tqdm(all_agencies):
            signal = repair_address(agency)
            if signal:
                repair_count += 1

        print(f'{repair_count} addresses replicated')

