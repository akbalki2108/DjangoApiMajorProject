from django.db import models

# Create your models here.

# Create your models here.

class Person(models.Model):
    firstname = models.CharField(max_length=20, default='')
    lastname = models.CharField(max_length=20, default='')
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    adhaar = models.BigIntegerField(primary_key=True)
    email = models.EmailField(default='abc@ycce.in')
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.firstname + " " + self.lastname

class Voter(models.Model):
    epic = models.CharField(max_length=20, unique=True,default = '0')  # Assuming EPIC number is a string
    fingerprint = models.CharField(max_length=1024,default = '0')
    status = models.CharField(max_length=50,default = '0')
    disability = models.BooleanField(default=False)

    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.person.firstname + " " + self.person.lastname + "( " + str(self.person.adhaar) + " )"

class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    party = models.CharField(max_length=20)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    manifesto = models.FileField(upload_to='manifestos/', null=True, blank=True, default='default_pdf.pdf')
    image = models.ImageField(upload_to='profile/', null=True, default='default_image.jpg')
    accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.person.firstname + " " + self.person.lastname + "( " + self.party + " )"


class Machine(models.Model):
    machine_no = models.CharField(max_length=20, primary_key=True)
    location = models.CharField(max_length=100)
    local_ip = models.CharField(max_length=15)

    def __str__(self):
        return f"Machine {self.machine_no}"

class ElectionData(models.Model):
    epic_id = models.CharField(max_length=20)
    transaction_no = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Election Data: EPIC ID - {self.epic_id}, Transaction No. - {self.transaction_no}"
    

class ToggleSettings(models.Model):
    election_toggle = models.BooleanField(default=False)
    voter_registration_toggle = models.BooleanField(default=False)
    candidate_registration_toggle = models.BooleanField(default=False)


from django.db import models
from django.db.models import Count

class ElectionDetails(models.Model):
    date = models.IntegerField(default=0)
    num_candidates = models.IntegerField(default=0)
    candidate_ids = models.TextField(default='')  # Store as comma-separated list
    party_names = models.TextField(default='')  # Store as comma-separated list
    num_machines = models.IntegerField(default=0)
    machine_ids = models.TextField(default='')  # Store as comma-separated list

    @classmethod
    def create(cls, date):
        # Calculate necessary details
        candidates = Candidate.objects.all()
        candidate_ids = ','.join(str(candidate.id) for candidate in candidates)
        party_names = ','.join(candidate.party for candidate in candidates)
        num_candidates = candidates.count()

        machines = Machine.objects.all()
        machine_ids = ','.join(machine.machine_no for machine in machines)
        num_machines = machines.count()

        return cls.objects.create(
            date=date,
            num_candidates=num_candidates,
            candidate_ids=candidate_ids,
            party_names=party_names,
            num_machines=num_machines,
            machine_ids=machine_ids
        )

    # def update_details(self):
    #     candidates = Candidate.objects.all()
    #     self.num_candidates = candidates.count()
    #     self.candidate_ids = ','.join(str(candidate.id) for candidate in candidates)
    #     self.party_names = ','.join(candidate.party for candidate in candidates)

    #     machines = Machine.objects.all()
    #     self.num_machines = machines.count()
    #     self.machine_ids = ','.join(machine.machine_no for machine in machines)

    #     self.save()

    def __str__(self):
        return f"Election Details - Date: {self.date}, Candidates: {self.num_candidates}, Machines: {self.num_machines}"
