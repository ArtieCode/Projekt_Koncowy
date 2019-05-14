from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import DetectiveAgencyRecord, DetectiveAgency, AgencyAddress
from inquisitor.management.commands._scraping_machinery import get_single_address, scrape_google


class AddressInitializer:

    def __init__(self, company_id, address_type, address_string):
        self.type = address_type
        self.owner = DetectiveAgency.objects.get(company_id=company_id)
        self.address_string = address_string

        self.defaults = {
            'address_type': self.type,
            'owner': self.owner,
            'raw_address': self.address_string
        }



class Command(BaseCommand):
    help = 'Gets address strings for each agency, processes them via google, and saves to DB'

    def handle(self, *args, **options):
        key = input('enter google api key: ')
        agencies = DetectiveAgency.objects.all()
        reg_added = 0
        active_added = 0
        last_processed_record = ""
        for agency in agencies:
            print(f"Last processed record: {last_processed_record}")
            print("Processing next address...")
            agency_record = agency.registry

            if len(agency.agencyaddress_set.values()) == 2:
                continue

            if agency_record.registered_address !="":
                processed_reg_address = get_single_address(agency_record.registered_address)
                if processed_reg_address !="":
                    scraped_address = scrape_google(processed_reg_address, key)
                    if scraped_address is None:
                        pass
                    else:
                        init = AddressInitializer(agency.company_id, 1, scraped_address)
                        db_entry = AgencyAddress.objects.update_or_create(raw_address=init.address_string, address_type=init.type, owner=init.owner, defaults=init.defaults)
                        if db_entry[1]:
                            reg_added += 1
                            print("REG ADDED")
                        print(processed_reg_address)
                        print(scraped_address)
                        last_processed_record = agency.company_id


            if agency_record.active_addresses !="":
                processed_active_address = get_single_address(agency_record.active_addresses)
                if processed_active_address !="":
                    active_address = agency_record.active_addresses
                    processed_active_address = get_single_address(active_address)
                    if processed_active_address != "":
                        scraped_address = scrape_google(processed_active_address, key)
                        if scraped_address is None:
                            pass
                        else:
                            init = AddressInitializer(agency.company_id, 2, scraped_address)
                            db_entry = AgencyAddress.objects.update_or_create(raw_address=init.address_string, address_type=init.type, owner=init.owner, defaults=init.defaults)
                            if db_entry[1]:
                                active_added += 1
                                print("ACTIVE ADDED")
                            print(scraped_address)
                            print(processed_active_address)
                            last_processed_record = agency.company_id










