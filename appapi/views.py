from .models import Person, Voter, Candidate, Machine, ElectionData,ToggleSettings, ElectionDetails,EpicIdData
from .serializers import PersonSerializer, CandidateSerializer, MachineSerializer, ElectionDataSerializer,ElectionDetailsSerializer,EpicIdDataSerializer

from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from web3 import Web3
from datetime import date

import os
import time
import json

from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404


blockchain_url = 'https://sepolia.infura.io/v3/ab071685741847ff8ab969312efc0cfe'

contract_abi = os.environ.get('CONTRACT_ABI')

w3 = Web3(Web3.HTTPProvider(blockchain_url))

@csrf_exempt
def get_election_date(request):
    try:

        if not w3.is_connected():
            return JsonResponse({'error': 'Web3 connection error'}, status=500)
        
        contract_address = os.environ.get('CONTRACT_ADDRESS')

        contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)

        allDates = contract_instance.functions.getAllInactiveDates().call()
        print(allDates)
        
        return JsonResponse({"dates": allDates}, status=200,safe = False)
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def end_election(request):
    try:

        if not w3.is_connected():
            return JsonResponse({'error': 'Web3 connection error'}, status=500)
        
        contract_address = os.environ.get('CONTRACT_ADDRESS')
        mywallet = os.environ.get('MY_WALLET')
        myprivatekey = os.environ.get('PRIVATE_KEY')

        contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)

        chain_id = w3.eth.chain_id

        txn_params = {
            'to': contract_instance.address,  
            'from': mywallet,  # Replace with your wallet address
            'gas': 3000000,  # Adjust gas limit as necessary
            'nonce': w3.eth.get_transaction_count(mywallet),
            'data': contract_instance.encodeABI('endLastElection'),
            'maxFeePerGas': w3.to_wei(250, 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei(2, 'gwei'),
            'chainId': chain_id,
        }
        
        signed_txn = w3.eth.account.sign_transaction(txn_params, private_key=myprivatekey)

        # Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # print(tx_hash)

        ToggleSettings.objects.update(election_toggle=False)

        return JsonResponse("Election ended successfully!", status=200,safe = False)
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_result(request):

    try:

        if not w3.is_connected():
            return JsonResponse({'error': 'Web3 connection error'}, status=500)
        
        contract_address = os.environ.get('CONTRACT_ADDRESS')
        print(contract_address)
        contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)


        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        find_date = body_data.get('date')

        result = contract_instance.functions.getAllCandidates(int(find_date)).call()
        
        formatted_result = []

        if result:

            transposed_result = list(zip(*result))

            for candidate_data in transposed_result:
                candidate_dict = {
                    'candidateId': candidate_data[0],
                    'partyName': candidate_data[1],
                    'vote': candidate_data[2]
                }
                formatted_result.append(candidate_dict)

        return JsonResponse(formatted_result, status=200,safe = False)
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
        # _date = 1648876800
        # _num_candidates = 3
        # _candidate_ids = [1, 2, 3]
        # _party_names = ["Party A", "Party B", "Party C"]
        # _num_machines = 2
        # _machine_ids = [101, 102]

        _date = unix_timestamp
        _num_candidates = candidates.count()
        _candidate_ids = candidate_ids
        _party_names = candidate_party_names
        _num_machines = machines.count()
        _machine_ids = machine_ids


        # Convert Python list to array of uint256
        _candidate_ids = list(map(int, candidate_ids))
        _machine_ids = list(map(int, machine_ids))

        # Convert Python list to array of string
        _party_names = list(map(str, candidate_party_names))



        # print(f"_date: {type(_date)}, {_date}")
        # print(f"_num_candidates: {type(_num_candidates)}, {_num_candidates}")
        # print(f"_candidate_ids: {type(_candidate_ids)}, {_candidate_ids}")
        # print(f"_party_names: {type(_party_names)}, {_party_names}")
        # print(f"_num_machines: {type(_num_machines)}, {_num_machines}")
        # print(f"_machine_ids: {type(_machine_ids)}, {_machine_ids}")
        
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

        # Saving ElectionDetails instance
        election_details = ElectionDetails(date=_date, num_candidates=_num_candidates,
                                           candidate_ids=",".join(map(str, candidate_ids)),
                                           party_names=",".join(candidate_party_names),
                                           num_machines=_num_machines,
                                           machine_ids=",".join(map(str, machine_ids)))
        election_details.save()
        
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

from random import choice

@api_view(['GET'])
def get_epicid(request):
    if request.method == 'GET':
        try:
            unallotted_epicids = EpicIdData.objects.filter(allotted=False)
            
            if unallotted_epicids.exists():
                random_epicid = choice(unallotted_epicids).epic_id
                return Response({'random_epicid': random_epicid}, status=200)
            else:
                return Response({'error': 'No unallotted epic ids available'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)





@api_view(['POST'])
def add_card(request):
        if request.method == 'POST':
            data = request.data

            try:

                epicId = EpicIdData.objects.create(
                            epic_id = data['epic_id'],
                        )
                
                return Response({'message': 'Card added successfully'}, status=201)
            except Exception as e:
                return Response({'error': str(e)}, status=400)



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
                
                epic_id_data = EpicIdData.objects.get(epic_id=data['epic'])
                epic_id_data.allotted = True
                epic_id_data.save()

                # Construct the email message
                subject = f"Voter Registration Successful - {data['epic']}"

                message = f"Dear {data['firstname']},\n\n"\
                        f"We are pleased to inform you that your voter registration for the upcoming election has been successful. Your EPIC ID CARD has been generated, which you will need to present at the polling station on the day of the election.\n\n"\
                        f"Your EPIC ID: {data['epic']}\n\n"\
                        f"Please keep this EPIC ID safe, as it will be required for verification during the voting process.\n\n"\
                        f"For any further information or assistance, please visit our website or contact us directly.\n\n"\
                        f"Thank you for participating in the democratic process.\n\n"\
                        f"Best regards,\n"\
                        f"iMatdaan Team"
            

                print(data['email'])
                send_mail(
                    subject,
                    message,
                    'settings.EMAIL_HOST_USER',  # Use a no-reply email address
                    [data['email']],
                    fail_silently=False
                )
                
                return Response({'message': 'Person created successfully'}, status=201)
            except Exception as e:
                return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def candidate_count(request):
    count_can = Candidate.objects.all().count()
    return HttpResponse(count_can, content_type='text/plain')

@api_view(['POST'])
def create_person_with_candidation(request):
    if request.method == 'POST':

        # data = request.data
        # print(data)
        # try:
        #     person = Person.objects.create(
        #         firstname=data['firstname'],
        #         lastname=data['lastname'],
        #         dob=data['dob'],
        #         gender=data['gender'],
        #         adhaar=data['adhaar'],
        #         email=data['email'],
        #         phone=data['phone']
        #     )

        #     candidate = Candidate.objects.create(
        #         party= data['party'],
        #         manifesto= data['manifesto'],
        #         image=data['image'],
        #         accepted=data['accepted'],
        #     )
            
            # Construct the email message
            # subject = 'Candidate Registration Successful - Verification Required'

            # message = f"Dear {data['firstname']},\n\n"\
            #           f"Congratulations on successfully registering as a candidate for the upcoming election.\n\n"\
            #           f"Please note your candidate ID for future reference: [Candidate ID]\n\n"\
            #           f"Before [Date], as announced on our website, you are required to visit the Election Commissioner's office for verification and confirmation of your candidacy. Please ensure you bring all necessary documents as outlined in the Election Process & Guidelines available on the iMatdaan website.\n\n"\
            #           f"For any questions or assistance, please contact us directly.\n\n"\
            #           f"Thank you for your participation in the electoral process.\n\n"\
            #           f"Best regards,\n"\
            #           f"iMatdaan Team"
        

            # print(data['email'])
            # send_mail(
            #     subject,
            #     message,
            #     'settings.EMAIL_HOST_USER',  # Use a no-reply email address
            #     [data['email']],
            #     fail_silently=False
            # )
            
        #     return Response({'message': 'Person with candidation created successfully!!'}, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

             
        person_serializer = PersonSerializer(data=request.data)
        candidate_serializer = CandidateSerializer(data=request.data)
        if person_serializer.is_valid() and candidate_serializer.is_valid():
            person_instance = person_serializer.save()
            candidate_instance = candidate_serializer.save(person=person_instance)
            

            subject = 'Candidate Registration Successful - Verification Required'

            message = f"Dear {person_instance.firstname},\n\n"\
                      f"Congratulations on successfully registering as a candidate for the upcoming election.\n\n"\
                      f"Please note your candidate ID for future reference: {candidate_instance.id}\n\n"\
                      f"Before [Date], as announced on our website, you are required to visit the Election Commissioner's office for verification and confirmation of your candidacy. Please ensure you bring all necessary documents as outlined in the Election Process & Guidelines available on the iMatdaan website.\n\n"\
                      f"For any questions or assistance, please contact us directly.\n\n"\
                      f"Thank you for your participation in the electoral process.\n\n"\
                      f"Best regards,\n"\
                      f"iMatdaan Team"
            

            print(message)
            print(person_instance.email)

            send_mail(
                subject,
                message,
                'settings.EMAIL_HOST_USER',  # Use a no-reply email address
                [person_instance.email],
                fail_silently=False
            )
            
            return Response({'message': 'Person with candidation created successfully!!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['DELETE'])
def delete_all_candidates(request):
    try:
        candidates = Candidate.objects.all()
        candidates.delete()
        return JsonResponse({'message': 'All candidates deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['PUT'])
def accept_candidate(request, candidate_id):
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        candidate.accepted = True
        candidate.save()
        return JsonResponse({'message': f'Candidate {candidate_id} accepted successfully'}, status=200)
    except Candidate.DoesNotExist:
        return JsonResponse({'error': f'Candidate with id {candidate_id} does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['DELETE'])
def delete_candidate(request, candidate_id):
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        candidate.delete()
        return JsonResponse({'message': f'Candidate {candidate_id} deleted successfully'}, status=200)
    except Candidate.DoesNotExist:
        return JsonResponse({'error': f'Candidate with id {candidate_id} does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

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

    def create(self, request, *args, **kwargs):
        # First, let's handle creating the ElectionData
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            epic_id = serializer.validated_data.get('epic_id')
            machine_no = request.data.get('machine_no')
            print(machine_no)
            location = None  # Initialize location to None

            if machine_no:
                try:
                    machine = Machine.objects.get(machine_no=machine_no)
                    location = machine.location
                except Machine.DoesNotExist:
                    raise Http404("Machine matching query does not exist.")            
            # Ensure location is not None
            if location is None:
                location = ""  # Set a default value for location if it's None
            
            serializer.validated_data['location'] = location  # Update location in validated data
            
            # Continue with saving the serializer
            serializer.save()
            
            if epic_id:
                try:
                    voter = Voter.objects.get(epic=epic_id)
                    voter.status = 1  # You should replace this with your logic to update status
                    voter.save()
                    print(voter.person.email)
                    send_mail(
                       'Your vote has been recorded',
                        'Dear voter, your vote has been successfully recorded.',
                        'settings.EMAIL_HOST_USER',  # Use a no-reply email address
                        [voter.person.email],
                        fail_silently=False
                    )
                    
                except Voter.DoesNotExist:
                    pass  # Handle the case where voter with epic_id doesn't exist

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    

class ElectionDetailsRetrieve(generics.ListAPIView):
    serializer_class = ElectionDetailsSerializer
    lookup_field = 'date'

    def get_queryset(self):
        date = self.kwargs.get('date')
        queryset = ElectionDetails.objects.filter(date=date)
        
        if not queryset.exists():
            raise ValidationError('No ElectionDetails instance found for the given date')
        
        return queryset
    

@api_view(['POST'])
def update_toggle_settings(request):

    print(request.data)
    try:
        toggle_name = request.data.get('toggle_name')
        toggle_value = request.data.get('toggle_value')

        if toggle_value == 'true':
            toggle_value = True
        else:
            toggle_value = False

        # Update the corresponding toggle setting in the database
        toggle_settings = ToggleSettings.objects.first()  # Assuming only one instance of ToggleSettings

        if hasattr(toggle_settings, toggle_name):
            setattr(toggle_settings, toggle_name, toggle_value)
            toggle_settings.save()
            return JsonResponse({'message': 'Toggle settings updated successfully.'},status=200)
        else:
            return JsonResponse({'error': f'Toggle setting "{toggle_name}" does not exist.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['GET'])
def get_toggle_settings(request):
    try:
        toggle_settings = ToggleSettings.objects.first()

        data = {
            'election_toggle': toggle_settings.election_toggle,
            'voter_registration_toggle': toggle_settings.voter_registration_toggle,
            'candidate_registration_toggle': toggle_settings.candidate_registration_toggle
        }
        
        
        return JsonResponse(data,safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)