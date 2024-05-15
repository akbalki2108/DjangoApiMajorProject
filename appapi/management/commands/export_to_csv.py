import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from appapi.models import Person, Voter, Candidate, Machine, ElectionData, ToggleSettings, ElectionDetails, EpicIdData

class Command(BaseCommand):
    help = 'Export data to CSV files'

    def handle(self, *args, **options):
        # Create a folder named 'csv' if it doesn't exist
        csv_dir = os.path.join(settings.BASE_DIR, 'csv')
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        self.export_model(Person, os.path.join(csv_dir, 'persons.csv'))
        self.export_model(Voter, os.path.join(csv_dir, 'voters.csv'))
        self.export_model(Candidate, os.path.join(csv_dir, 'candidates.csv'))
        self.export_model(Machine, os.path.join(csv_dir, 'machines.csv'))
        self.export_model(ElectionData, os.path.join(csv_dir, 'election_data.csv'))
        self.export_model(ToggleSettings, os.path.join(csv_dir, 'toggle_settings.csv'))
        self.export_model(ElectionDetails, os.path.join(csv_dir, 'election_details.csv'))
        self.export_model(EpicIdData, os.path.join(csv_dir, 'epic_id_data.csv'))

    def export_model(self, model, file_name):
        queryset = model.objects.all()
        model_fields = [field.name for field in model._meta.fields]

        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(model_fields)  # Write headers

            for obj in queryset:
                writer.writerow([getattr(obj, field) for field in model_fields])

        self.stdout.write(self.style.SUCCESS(f'Successfully exported {model.__name__} to {file_name}'))
