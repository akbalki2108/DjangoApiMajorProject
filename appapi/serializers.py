# serializers.py
from rest_framework import serializers
from .models import Person, Candidate,Machine, ElectionData

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'

class ElectionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionData
        fields = '__all__'
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['firstname', 'lastname', 'dob', 'gender', 'adhaar', 'email', 'phone']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['party', 'manifesto', 'profile', 'accepted']