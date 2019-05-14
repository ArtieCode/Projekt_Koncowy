from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import AgencyAddress, DetectiveAgency
from tqdm import tqdm
import copy
import re


class Command(BaseCommand):
    help = 'Count agencies without a valid address'

    def handle(self, *args, **options):
        all_agencies = DetectiveAgency.objects.all()
        replication_count = 0

        def replicate_address(db_object):
            addresses = db_object.agencyaddress_set.all()

            if addresses is not None:

                has_registered_address = None
                has_active_address = None

                for address in addresses:
                    address_type = address.address_type
                    if address_type == 1:
                        has_registered_address = True
                    if address_type == 2:
                        has_active_address = True

                    if has_registered_address and not has_active_address:
                        replicated_address = copy.deepcopy(address)
                        replicated_address.address_type = 2
                        replicated_address.save()
                        return True

            return False

        for agency in tqdm(all_agencies):
            signal = replicate_address(agency)
            if signal:
                replication_count += 1

        print(f'{replication_count} addresses replicated')

