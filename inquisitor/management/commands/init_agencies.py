from django.core.management.base import BaseCommand, CommandError
from inquisitor.models import DetectiveAgencyRecord, DetectiveAgency

class AgencyInitializer:

    def __init__(self, new_company_id, entry_ID, firm_name):
        self.company_id = new_company_id
        self.registry_id = entry_ID
        self.company_name = firm_name

        self.defaults = {
            'company_id': self.company_id,
            'registry_id': self.registry_id,
            'company_name': self.company_name

            }

class Command(BaseCommand):
    help = 'Scrapes detective records from BIP and updates the DB'

    def handle(self, *args, **options):
        all_records = DetectiveAgencyRecord.objects.all()
        print(f'Found {len(all_records)} registry records, attempting to create related agencies')
        company_id_prefix = "ZD00"
        counter = 0
        created = 0
        updated = 0

        for record in all_records:

            new_company_id = company_id_prefix + counter
            counter += 1
            entry_ID = record.entry_ID
            firm_name = record.firm_name

            init = AgencyInitializer(new_company_id, entry_ID, firm_name)
            db_entry = DetectiveAgency.objects.update_or_create(company_id=init.company_id, defaults=init.defaults)
            if db_entry[1]:
                created += 1
            else:
                updated += 1
            if counter % 100 == 0:
                print(f'{counter} records processed...')

        print(f'{created} records created, {updated} records updated.')






