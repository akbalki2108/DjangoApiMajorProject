from rest_framework import viewsets
from .models import Person, Voter, Candidate, Machine, ElectionData
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
from .models import Voter

@api_view(['GET'])
def get_all_candidates(request):
    print("Hey i am in functuon")
    candidates = Candidate.objects.all()

    data = []
    print(f'{"Field name":20} {"Column name"}')
    print(50 * '-')
    for f in Candidate._meta.fields:
        print(f'{f.name:20} {f.db_column or f.attname}')
    for candidate in candidates:
        print(candidate)
        candidate_data = {
            'id':candidate.id,
            'party': candidate.party,
            'firstname': candidate.person.firstname,
            'lastname': candidate.person.lastname,
            'dob': str(candidate.person.dob),
            'gender': candidate.person.gender,
            'adhaar': candidate.person.adhaar,
            'email': candidate.person.email,
            'phone': candidate.person.phone,
            'manifesto': str(candidate.manifesto),
            'image': str(candidate.image),
            'accepted': candidate.accepted
        }
        data.append(candidate_data)
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def get_voter(request, epic_id):
    try:
        voter = Voter.objects.get(epic=epic_id)
        data = {
            'epic_id': voter.epic,
            'fingerprint': voter.fingerprint,
            'status': voter.status,
            'disability': voter.disability,
            'firstname': voter.person.firstname,
            'lastname': voter.person.lastname,
            'dob': str(voter.person.dob),
            'gender': voter.person.gender,
            'adhaar': voter.person.adhaar,
            'email': voter.person.email,
            'phone': voter.person.phone,
        }
        return JsonResponse(data)
    except Voter.DoesNotExist:
        return JsonResponse({'error': 'Voter not found'}, status=404)



@api_view(['GET'])
def get_all_voters(request):
    try:
        voters = Voter.objects.all()

        data = []

        for voter in voters:
            print(voter)

            voter_data = {
                'epic_id': voter.epic,
                'fingerprint': voter.fingerprint,
                'status': voter.status,
                'disability': voter.disability,
                'firstname': voter.person.firstname,
                'lastname': voter.person.lastname,
                'dob': str(voter.person.dob),
                'gender': voter.person.gender,
                'adhaar': voter.person.adhaar,
                'email': voter.person.email,
                'phone': voter.person.phone,
            }
            data.append(voter_data)
        return JsonResponse(data,safe=False)
    except Voter.DoesNotExist:
        return JsonResponse({'error': 'Voter not found'}, status=404)



@api_view(['GET'])
def get_election_data(request):
    try:
        election_data = ElectionData.objects.all()

        data = []

        for ed in election_data:
            print(ed)

            ed_data = {
                'epic_id': ed.epic,
                'transaction_no': ed.transaction_no,
                'date': ed.date,
                'location': ed.location,
            }
            data.append(ed_data)
        return JsonResponse(data,safe=False)
    except Voter.DoesNotExist:
        return JsonResponse({'error': 'Election data not found'}, status=404)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(['PUT'])
def update_voter_status(request, epic_id):
    try:
        voter = Voter.objects.get(epic=epic_id)
    except Voter.DoesNotExist:
        return JsonResponse({"message": "Voter not found"}, status=404)

    # Update the status based on the data sent in the request body
    new_status = request.data.get('status', voter.status)
    # Assuming 'status' is a field in your Voter model
    voter.status = new_status
    voter.save()

    return JsonResponse({"message": "Voter status updated successfully"}, status=200)


@api_view(['GET'])
def get_all_machines(request):
    try:
        machines = Machine.objects.all()

        data = []

        for machine in machines:
            # print(machine)

            machine_data = {
                'machine_no': machine.machine_no,
                'location': machine.location,
                'local_ip': machine.local_ip,
            }
            data.append(machine_data)
        return JsonResponse(data,safe=False)
    except Voter.DoesNotExist:
        return JsonResponse({'error': 'Voter not found'}, status=404)


@api_view(['POST'])
def personvoter(request):
        if request.method == 'POST':
            data = request.data
            try:
                person = Person.objects.create(
                    firstname=data['firstname'],
                    lastname=data['lastname'],
                    dob=data['dob'],
                    gender=data['gender'],
                    adhaar=data['adhaar'],
                    email=data['email'],
                    phone=data['phone']
                )
                voter = Voter.objects.create(
                    epic=data['epic'],
                    fingerprint=data.get('fingerprint', '0'),  # Default '0' if fingerprint not provided
                    status=data.get('status', '0'),  # Default '0' if status not provided
                    disability=data.get('disability', False),  # Default False if disability not provided
                    person=person  # Assign the created person to the voter
                )
                return Response({'message': 'Person created successfully'}, status=201)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
from django.http import HttpResponse

def candidate_count(request):
    count_can = Candidate.objects.all().count()
    return HttpResponse(count_can, content_type='text/plain')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def create_person_with_candidation(request):
    if request.method == 'POST':
        try:
            # Extract data from the request
            data = request.POST
            
            # Create a person
            person = Person.objects.create(
                firstname=data.get('firstname'),
                lastname=data.get('lastname'),
                dob=data.get('dob'),
                gender=data.get('gender'),
                adhaar=data.get('adhaar'),
                email=data.get('email'),
                phone=data.get('phone')
            )
            
            # Create a candidation  
            print(data.get('image'))
            candidate = Candidate.objects.create(
                party=data.get('party'),
                manifesto=data.get('manifesto'),
                image=data.get('image'),
                accepted=data.get('accepted'),
                person=person
            )
            
            return JsonResponse({'message': 'Person with candidation created successfully'}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person, Candidate
from .serializers import PersonSerializer, CandidateSerializer

@api_view(['POST'])
def create_person_with_candidation(request):
    if request.method == 'POST':
        person_serializer = PersonSerializer(data=request.data)
        candidate_serializer = CandidateSerializer(data=request.data)

        if person_serializer.is_valid() and candidate_serializer.is_valid():
            person_instance = person_serializer.save()
            candidate_instance = candidate_serializer.save(person=person_instance)
            return Response({'message': 'Person with candidation created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


from rest_framework import generics
from .models import Machine, ElectionData
from .serializers import MachineSerializer, ElectionDataSerializer

class MachineListCreate(generics.ListCreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class MachineRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class ElectionDataListCreate(generics.ListCreateAPIView):
    queryset = ElectionData.objects.all()
    serializer_class = ElectionDataSerializer

class ElectionDataRetrieve(generics.RetrieveAPIView):
    queryset = ElectionData.objects.all()
    serializer_class = ElectionDataSerializer