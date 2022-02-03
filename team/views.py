from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from team.models import FavNurse, FavTraineeSurgeon, FavAnesthesiologist
from user.models import Surgeon, Nurse, TraineeSurgeon, Anesthesiologist
from rest_framework.response import Response


@csrf_exempt
@api_view(['POST'])
def get_my_team_details(request):
    if request.method == 'POST':
        token = JSONParser().parse(request)['key']
        if (Token.objects.filter(key=token).exists()):
            tObject = Token.objects.get(key=token)
            user = tObject.user
            surgeon = Surgeon.objects.get(user=user)
            fav_all_nurse = []
            fav_all_trainee_surgeon = []
            fav_all_anesthesiologist = []

            all_nurse = []
            all_trainee_surgeon = []
            all_anesthesiologist = []

            for o in FavNurse.objects.filter(surgeon=surgeon):
                fav_all_nurse.append(o.nurse.title + " " + o.nurse.first_name + " " + o.nurse.last_name)

            for o in FavTraineeSurgeon.objects.filter(surgeon=surgeon):
                fav_all_trainee_surgeon.append(o.trainee_surgeon.title + " " + o.trainee_surgeon.first_name + " " + o.trainee_surgeon.last_name)

            for o in FavAnesthesiologist.objects.filter(surgeon=surgeon):
                fav_all_anesthesiologist.append(o.anesthesiologist.title + " " + o.anesthesiologist.first_name + " " + o.anesthesiologist.last_name)

            for o in Nurse.objects.all():
                all_nurse.append(o.title + " " + o.first_name + " " + o.last_name)

            for o in TraineeSurgeon.objects.all():
                all_trainee_surgeon.append(o.title + " " + o.first_name + " " + o.last_name)

            for o in Anesthesiologist.objects.all():
                all_anesthesiologist.append(o.title + " " + o.first_name + " " + o.last_name)

            all = {
                'nurse': all_nurse,
                'trainee_surgeon': all_trainee_surgeon,
                'anesthesiologist': all_anesthesiologist,
                'fav_nurse': fav_all_nurse,
                'fav_trainee_surgeon': fav_all_trainee_surgeon,
                'fav_anesthesiologist': fav_all_anesthesiologist
            }

            print('///// ------ alL team details ------- /////////')
            print(all)

            return Response(all, status=status.HTTP_200_OK, exception=False)


@csrf_exempt
@api_view(['POST'])
def create_team(request):
    if request.method == 'POST':
        print('CREATE TEAM ///////////////////////////////////')
        request_data = JSONParser().parse(request)
        token = request_data['key']
        fav_team = request_data['favTeam']
        if (Token.objects.filter(key=token).exists()):
            tObject = Token.objects.get(key=token)
            user = tObject.user
            user_data = {
                'user_id': user.pk,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_medical_staff': user.is_medical_staff,
                'is_admin_staff': user.is_admin_staff,
                'role': user.role
            }
            user_profile_data = {}
            profile = Surgeon.objects.get(user=user)
            for trainee_surgeon in fav_team['trainee_surgeon']:
                pass
            for anesthesiologists in fav_team['anesthesiologists']:
                pass
            for nurse in fav_team['nurse']:
                print("FaV NURSE CALL HERE")
                nurse_names = nurse.split(' ')
                nurse = Nurse.objects.get(first_name=nurse_names[1], last_name=nurse_names[2])
                FavNurse.objects.create(surgeon=profile, nurse=nurse)
            user_data['profile'] = user_profile_data
            return Response(user_data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)
