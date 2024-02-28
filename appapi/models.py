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
    machine_no = models.CharField(max_length=20, unique=True)
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