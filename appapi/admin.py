from django.contrib import admin
from .models import Person, Voter, Candidate, Machine, ElectionData

# Register your models here.
admin.site.register(Person)
admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(Machine)
admin.site.register(ElectionData)
