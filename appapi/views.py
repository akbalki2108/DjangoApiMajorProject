from rest_framework import viewsets
from .models import Person, Voter, Candidate, Machine, ElectionData
from django.http import HttpResponse
from rest_framework.decorators import api_view

from django.http import JsonResponse
from .models import Voter
from django.views.decorators.csrf import csrf_exempt

import os


from web3 import Web3

from datetime import date
import time

blockchain_url = 'https://sepolia.infura.io/v3/ab071685741847ff8ab969312efc0cfe'

contract_abi =[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_date",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_numCandidates",
				"type": "uint256"
			},
			{
				"internalType": "uint256[]",
				"name": "_candidateIds",
				"type": "uint256[]"
			},
			{
				"internalType": "string[]",
				"name": "_partyNames",
				"type": "string[]"
			},
			{
				"internalType": "uint256",
				"name": "_numMachines",
				"type": "uint256"
			},
			{
				"internalType": "uint256[]",
				"name": "_machineIds",
				"type": "uint256[]"
			}
		],
		"name": "startElection",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_date",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_machineId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_candidateId",
				"type": "uint256"
			}
		],
		"name": "vote",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "elections",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "date",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "numCandidates",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "numMachines",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_date",
				"type": "uint256"
			}
		],
		"name": "getAllCandidates",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			},
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			},
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_date",
				"type": "uint256"
			}
		],
		"name": "getAllMachines",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			},
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			},
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_date",
				"type": "uint256"
			}
		],
		"name": "getTotalCandidates",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_date",
				"type": "uint256"
			}
		],
		"name": "getTotalMachines",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

w3 = Web3(Web3.HTTPProvider(blockchain_url))

@csrf_exempt
def start_election(request):

    try:

        if not w3.is_connected():
            return JsonResponse({'error': 'Web3 connection error'}, status=500)
    
        contract_address = os.environ.get('CONTRACT_ADDRESS')
        mywallet = os.environ.get('MY_WALLET')
        myprivatekey = os.environ.get('PRIVATE_KEY')

        #create instance
        contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)

        today = date.today()
        unix_timestamp = int(time.mktime(today.timetuple()))
        print(unix_timestamp)

        candidates = Candidate.objects.all()
        machines = Machine.objects.all()

        candidate_ids = list(Candidate.objects.values_list('id', flat=True))
        # print("All candidate IDs:", candidate_ids)

        candidate_party_names = list(Candidate.objects.values_list('party', flat=True))
        # print("All candidate party names:", candidate_party_names)

        machine_ids = list(Machine.objects.values_list('machine_no', flat=True))
        # print("All machine IDs:", machine_ids)


        # Example parameters
        _date = unix_timestamp
        _num_candidates = candidates.count()
        _candidate_ids = candidate_ids
        _party_names = candidate_party_names
        _num_machines = machines.count()
        _machine_ids = machine_ids

        print(f"_date: {type(_date)}, {_date}")
        print(f"_num_candidates: {type(_num_candidates)}, {_num_candidates}")
        print(f"_candidate_ids: {type(_candidate_ids)}, {_candidate_ids}")
        print(f"_party_names: {type(_party_names)}, {_party_names}")
        print(f"_num_machines: {type(_num_machines)}, {_num_machines}")
        print(f"_machine_ids: {type(_machine_ids)}, {_machine_ids}")
        
        chain_id = w3.eth.chain_id

        txn_params = {
            'to': contract_instance.address,  
            'from': mywallet,  # Replace with your wallet address
            'gas': 3000000,  # Adjust gas limit as necessary
            'nonce': w3.eth.get_transaction_count(mywallet),
            'data': contract_instance.encodeABI('startElection', [_date, _num_candidates, _candidate_ids, _party_names, _num_machines, _machine_ids]),
            'maxFeePerGas': w3.to_wei(250, 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei(2, 'gwei'),
            'chainId': chain_id,
        }
        
        signed_txn = w3.eth.account.sign_transaction(txn_params, private_key=myprivatekey)

        # Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # print(tx_hash)

        # Wait for the transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # print("Transaction successful:", tx_receipt)
        
        return JsonResponse({"message": "Election started successfully!"}, status=200)
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@api_view(['GET'])
def get_all_candidates(request):
    # print("Hey i am in functuon")
    candidates = Candidate.objects.all()
    
    data = []
    # print(f'{"Field name":20} {"Column name"}')
    # print(50 * '-')
    for f in Candidate._meta.fields:
        print(f'{f.name:20} {f.db_column or f.attname}')
    for candidate in candidates:
        # print(candidate)
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
            # print(voter)

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
            # print(ed)

            ed_data = {
                'epic_id': ed.epic_id,
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

def candidate_count(request):
    count_can = Candidate.objects.all().count()
    return HttpResponse(count_can, content_type='text/plain')

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
            return Response({'message': 'Person with candidation created successfully!!'}, status=status.HTTP_201_CREATED)
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
    lookup_field = 'machine_no' 

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # Update only the IP address
        instance.local_ip = serializer.validated_data.get('local_ip', instance.local_ip)
        self.perform_update(serializer)
        return Response(serializer.data)
    

class ElectionDataListCreate(generics.ListCreateAPIView):
    queryset = ElectionData.objects.all()
    serializer_class = ElectionDataSerializer


from rest_framework.exceptions import ValidationError
from .models import ElectionData

class ElectionDataRetrieve(generics.ListAPIView):
    # queryset = ElectionData.objects.all()
    serializer_class = ElectionDataSerializer
    lookup_field = 'date'

    def get_queryset(self):
        date = self.kwargs.get('date')
        queryset = ElectionData.objects.filter(date=date)
        
        if not queryset.exists():
            raise ValidationError('No ElectionData instance found for the given date')
        
        return queryset