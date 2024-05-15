import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from appapi.models import Person, Voter, Candidate

class Command(BaseCommand):
    help = 'Upload data for Person, Voter, and Candidate models from CSV files'

    def handle(self, *args, **options):
        csv_dir = os.path.join(settings.BASE_DIR, 'csv')
        if not os.path.exists(csv_dir):
            self.stdout.write(self.style.ERROR(f'Directory {csv_dir} does not exist'))
            return

        self.upload_persons(os.path.join(csv_dir, 'persons.csv'))
        # self.link_candidates_to_persons(os.path.join(csv_dir, 'candidates.csv'))
        self.upload_voters(os.path.join(csv_dir, 'voters.csv'))

    def upload_persons(self, file_name):
        if not os.path.exists(file_name):
            self.stdout.write(self.style.ERROR(f'File {file_name} does not exist'))
            return

        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                person = Person()
                person.firstname = row['firstname']
                person.lastname = row['lastname']
                person.dob = row['dob']
                person.gender = row['gender']
                person.adhaar = row['adhaar']
                person.email = row['email']
                person.phone = row['phone']
                person.save()
            
        print("Persons uploaded")

    def upload_voters(self, file_name):
        if not os.path.exists(file_name):
            self.stdout.write(self.style.ERROR(f'File {file_name} does not exist'))
            return

        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                adhaar = row['adhaar']
                print(adhaar)
                person = Person.objects.get(adhaar=adhaar)
                print("hey")
                if person:
                    # voter = Voter()
                    # voter.epic = row['epic']
                    # voter.fingerprint = row['fingerprint']
                    # voter.status = row['status']
                    # voter.disability = row['disability']
                    # # Get the related person using the adhaar from the CSV
                    # voter.person = person
                    # voter.save()
                    Voter.objects.create(person=person, epic=row['epic'], fingerprint=row['fingerprint'],
                                        status=row['status'], disability=row['disability'])
                    print("Voter created for", person.firstname, person.lastname)

                    print("done")
                else:
                    self.stdout.write(self.style.ERROR(f'Person with adhaar={adhaar} not found'))

    def upload_candidates(self, file_name):
        if not os.path.exists(file_name):
            self.stdout.write(self.style.ERROR(f'File {file_name} does not exist'))
            return

        with open(file_name, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                candidate = Candidate()
                candidate.party = row['party']
                candidate.manifesto = row['manifesto']
                candidate.image = row['image']
                candidate.accepted = row['accepted']
                
                # Get the related person using the adhaar from the CSV
                person_adhaar = row['person_adhaar']
                person = Person.objects.get(adhaar=person_adhaar)
                candidate.person = person
                
                candidate.save()

        print("Candidates uploaded")
