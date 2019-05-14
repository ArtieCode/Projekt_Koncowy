from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import AgencyAddress
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Processes Google-formatted address strings into model fields'

    def handle(self, *args, **options):
        def process_address_string(db_object):
            raw_string = db_object.raw_address

            raw_split = raw_string.split(',')
            postcode_and_city = raw_split[1]

            db_object.street_address = raw_split[0]
            db_object.post_code = postcode_and_city[1:7]
            db_object.city = postcode_and_city[8:]

        all_addresses = AgencyAddress.objects.all()

        for address in tqdm(all_addresses):
            process_address_string(address)
            address.save()

