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
    path('machines/<int:pk>/', MachineRetrieveUpdateDestroy.as_view(), name='machine-retrieve-update-destroy'),
    path('electiondata/', ElectionDataListCreate.as_view(), name='electiondata-list-create'),
    path('electiondata/<int:pk>/', ElectionDataRetrieve.as_view(), name='electiondata-retrieve'),
    path('get_voter/<str:epic_id>/', get_voter, name='get_voter'),
    path('get_all_candidates/', get_all_candidates, name='get_all_candidates'),
    path('get_all_voters/', get_all_voters, name='get_all_voters'),
    path('candidate_count/', candidate_count, name='candidate_count'),
    path('get_all_machines/', get_all_machines, name='get_all_machines'),

    #hey i have changed on url
]
