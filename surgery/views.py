from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from surgery.models import Surgery, Patient
from team.models import FavNurse, FavTraineeSurgeon, FavAnesthesiologist
from user.models import Surgeon, Nurse, TraineeSurgeon, Anesthesiologist
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@csrf_exempt
@api_view(['POST'])
def get_predicted_results(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user
            surgeon = Surgeon.objects.get(user=user)

            data = {}
            return Response(data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def create_surgery(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user
            surgeon = Surgeon.objects.get(user=user)
            Surgery.objects.create()

            data = {}
            return Response(data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def create_surgery_team(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user

            surgeon_profile = Surgeon.objects.get(user=user)
            patient_details = request_data['patient_details']
            surgery_details = request_data['surgery_details']
            surgery_team_details = request_data['surgery_team_details']

            """ 
                start_minute = models.IntegerField()
                end_minute = models.IntegerField()
                start_hour = models.IntegerField()
                end_hour = models.IntegerField()
                date = models.IntegerField()
                month = models.IntegerField()  # Int or char?
                year = models.IntegerField()
                notes = models.TextField()
                surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
            
            """
            # Create Surgery Object
            surgery = Surgery.objects.create(
                start_minute=surgery_details['start_minute'],
                end_minute=surgery_details['end_minute'],
                start_hour=surgery_details['start_hour'],
                end_hour=surgery_details['end_hour'],
                date=surgery_details['date'],
                month=surgery_details['month'],
                year=surgery_details['year'],
                surgeon=surgeon_profile
            )
            surgery.save()

            patient = Patient.objects.create(
                first_name=patient_details['first_name'],
                last_name=patient_details['last_name'],
                address=patient_details['address'],
                email=patient_details['email'],
                telephone=patient_details['telephone'],
                age=patient_details['age'],
                gender=patient_details['gender'],
                weight=patient_details['weight'],
                height=patient_details['height'],
                cancer=patient_details['cancer'],
                cvd=patient_details['cvd'],
                dementia=patient_details['dementia'],
                diabetes=patient_details['diabetes'],
                digestive=patient_details['digestive'],
                osteoarthritis=patient_details['osteoarthritis'],
                pylogical=patient_details['pylogical'],
                pulmonary=patient_details['pulmonary'],
                surgery=surgery
            )
            patient.save()

            data = {}
            return Response(data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)
