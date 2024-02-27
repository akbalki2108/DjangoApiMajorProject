from rest_framework import viewsets
from .models import Person, Voter, Candidate, Machine, ElectionData
from rest_framework.response import Response
from rest_framework.decorators import api_view


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


def get_all_candidates(request):
    if request.method == 'GET':
        candidates = Candidate.objects.all()
        candidate_list = []
        for candidate in candidates:
            candidate_data = {
                'id': candidate.id,
                'firstname': candidate.person.firstname,
                'lastname': candidate.person.lastname,
                'dob': candidate.person.dob,
                'gender': candidate.person.gender,
                'adhaar': candidate.person.adhaar,
                'email': candidate.person.email,
                'phone': candidate.person.phone,
                'candidate_id': candidate.candidate_id,
                'party': candidate.party,
                'manifesto': candidate.manifesto.url if candidate.manifesto else None,
                'image': candidate.image.url if candidate.image else None,
                'accepted': candidate.accepted
            }
            candidate_list.append(candidate_data)
        return JsonResponse(candidate_list, safe=False)
    else:
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