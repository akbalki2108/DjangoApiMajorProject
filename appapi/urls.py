from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import *

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('personvoter/',personvoter,name="personvoter"),
    path('update_voter_status/<str:epic_id>/',update_voter_status, name='update_voter_status'),
    path('create_person_with_candidation/',create_person_with_candidation,name="create_person_with_candidation"),
    path('create_person_with_candidation1/', create_person_with_candidation, name='create_person_with_candidation1'),
    path('machines/', MachineListCreate.as_view(), name='machine-list-create'),
    path('machines/<int:machine_no>/', MachineRetrieveUpdateDestroy.as_view(), name='machine-retrieve-update-destroy'),
    path('electiondata/', ElectionDataListCreate.as_view(), name='electiondata-list-create'),
    path('electiondata/<str:date>/', ElectionDataRetrieve.as_view(), name='electiondata-retrieve'),
    path('election-details/<str:date>/', ElectionDetailsRetrieve.as_view(), name='election-details-retrieve'),
    path('get_voter/<str:epic_id>/', get_voter, name='get_voter'),
    path('get_all_candidates/', get_all_candidates, name='get_all_candidates'),
    path('get_all_voters/', get_all_voters, name='get_all_voters'),
    path('candidate_count/', candidate_count, name='candidate_count'),
    path('get_all_machines/', get_all_machines, name='get_all_machines'),
    path('get_election_data/', get_election_data, name='get_election_data'),
    path('start_election/', start_election, name='start_election'),
    path('update_toggle_settings/', update_toggle_settings, name='update_toggle_settings'),
    path('get_toggle_settings/', get_toggle_settings, name='get_toggle_settings'),
    path('get_election_date/', get_election_date, name='get_election_date'),
    path('get_result/', get_result, name='get_result'),
    path('end_election/', end_election, name='end_election'),
    path('add_card/', add_card, name='add_card'),
    path('get_epicid/', get_epicid, name='get_epicid'),
    path('delete_all_candidates/', delete_all_candidates, name='delete_all_candidates'),
    path('accept_candidate/', accept_candidate, name='accept_candidate'),
    path('delete_candidate/', delete_candidate, name='delete_candidate'),
    
    #hey i have changed on url
]
