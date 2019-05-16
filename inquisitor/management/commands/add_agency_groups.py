from django.core.management.base import BaseCommand
from inquisitor.models import DetectiveAgency
from tqdm import tqdm
from django.contrib.auth.models import Group, Permission



class Command(BaseCommand):
    help = 'repair address types'

    def handle(self, *args, **options):
        all_agencies = DetectiveAgency.objects.all()
        permission_set = [30, 32, 33, 34, 35, 36]

        for agency in tqdm(all_agencies):
            agency_group, created = Group.objects.get_or_create(name=agency.company_id)
            # Code to add permission to group ???
            for permission_number in permission_set:
                # Now what - Say I want to add 'Can add project' permission to new_group?
                permission = Permission.objects.get(id=permission_number)
                agency_group.permissions.add(permission)


