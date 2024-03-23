from django.contrib import admin
from .models import Person, Voter, Candidate, Machine, ElectionData,ToggleSettings,ElectionDetails

# Register your models here.
admin.site.register(Person)
admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(Machine)
admin.site.register(ElectionData)

class ToggleSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'election_toggle', 'voter_registration_toggle', 'candidate_registration_toggle')
    list_editable = ('election_toggle', 'voter_registration_toggle', 'candidate_registration_toggle')
    
    def save_model(self, request, obj, form, change):
        obj.save()
        
admin.site.register(ToggleSettings, ToggleSettingsAdmin)

admin.site.register(ElectionDetails)