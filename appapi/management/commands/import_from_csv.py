import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from appapi.models import Person, Voter, Candidate, Machine, ElectionData, ToggleSettings, ElectionDetails, EpicIdData

from django.db import models

class Command(BaseCommand):
    help = 'Import data from CSV files into the database'

    def handle(self, *args, **options):
        csv_dir = os.path.join(settings.BASE_DIR, 'csv')
        if not os.path.exists(csv_dir):
            self.stdout.write(self.style.ERROR(f'Directory {csv_dir} does not exist'))
            return

        # self.import_model(Person, os.path.join(csv_dir, 'persons.csv'))
        # self.import_model(Voter, os.path.join(csv_dir, 'voters.csv'))
        # self.import_model(Candidate, os.path.join(csv_dir, 'candidates.csv'))
        self.import_model(Machine, os.path.join(csv_dir, 'machines.csv'))
        self.import_model(ElectionData, os.path.join(csv_dir, 'election_data.csv'))
        self.import_model(ToggleSettings, os.path.join(csv_dir, 'toggle_settings.csv'))
        self.import_model(ElectionDetails, os.path.join(csv_dir, 'election_details.csv'))
        self.import_model(EpicIdData, os.path.join(csv_dir, 'epic_id_data.csv'))

    def import_model(self, model, file_name):
        if not os.path.exists(file_name):
            self.stdout.write(self.style.ERROR(f'File {file_name} does not exist'))
            return

        model_fields = [field.name for field in model._meta.fields]
        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Filter row to only include fields that exist in the model
                filtered_row = {key: value for key, value in row.items() if key in model_fields}

                # Convert fields to appropriate types
                for field in model._meta.fields:
                    if field.name in filtered_row:
                        try:
                            if isinstance(field, models.IntegerField):
                                filtered_row[field.name] = int(filtered_row[field.name])
                            elif isinstance(field, models.BooleanField):
                                filtered_row[field.name] = filtered_row[field.name].lower() in ['true', '1', 't', 'yes']
                        except ValueError as e:
                            self.stdout.write(self.style.ERROR(f"Invalid value for field '{field.name}': {filtered_row[field.name]}"))
                            continue

                try:
                    obj, created = model.objects.update_or_create(**filtered_row)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created {model.__name__} {obj}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated {model.__name__} {obj}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating/updating {model.__name__}: {e}'))
