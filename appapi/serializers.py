# serializers.py
from rest_framework import serializers
from .models import Person, Candidate,Machine, ElectionData,ElectionDetails,EpicIdData

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
        fields = ['party', 'manifesto', 'image', 'accepted']

class ElectionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionDetails
        fields = '__all__'


class EpicIdDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpicIdData
        fields = '__all__'