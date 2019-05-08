from django.core.management.base import BaseCommand, CommandError
from inquisitor.management.commands._scraping_machinery import scrape
from inquisitor.models import DetectiveAgencyRecord

class DetectiveRecord:

    def __init__(self, ID, entry_date, excision_date, firm, registered_address, NIP, active_address, voivodship):
        self.ID = ID
        self.entry_date = entry_date
        self.excision_date = excision_date
        self.firm = firm
        self.registered_address = registered_address
        self.nip_number = NIP
        self.active_address = active_address
        self.voivodship = voivodship

        if self.excision_date is not None:
            self.is_active = False
        else:
            self.is_active = True

        self.defaults = {
            'entry_ID': self.ID,
            'entry_date': self.entry_date,
            'excision_date': self.excision_date,
            'active_status': self.is_active,
            'firm_name': self.firm,
            'registered_address': self.registered_address,
            'active_addresses': self.active_address,
            'nip_number': self.nip_number,
            'voivodship': self.voivodship
            }

    def __str__(self):
        return str((self.ID,
                    self.entry_date,
                    self.excision_date,
                    self.is_active,
                    self.firm,
                    self.registered_address,
                    self.nip_number,
                    self.active_address,
                    self.voivodship))

class Command(BaseCommand):
    help = 'Scrapes detective records from BIP and updates the DB'

    def handle(self, *args, **options):
        scrape_results = scrape(0)
        print(f'Found {len(scrape_results)} records, processing...')
        created = 0
        updated = 0
        for result in scrape_results:
            if result != []:
                record = DetectiveRecord(*result)
                db_entry = DetectiveAgencyRecord.objects.update_or_create(entry_ID=record.ID, defaults=record.defaults)
                if db_entry[1]:
                    created += 1
                else:
                    updated += 1
        print(f'{created} records created, {updated} records updated.')




