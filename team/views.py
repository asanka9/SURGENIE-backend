from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from booked.models import BookedTraineeSurgeon, BookedAnesthesiologist, BookedNurse
from surgery.models import Surgery
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
            FavNurse.objects.filter(surgeon=profile).delete()
            FavTraineeSurgeon.objects.filter(surgeon=profile).delete()
            FavAnesthesiologist.objects.filter(surgeon=profile).delete()

            for trainee_surgeon in fav_team['trainee_surgeon']:
                trainee_surgeon_names = trainee_surgeon.split(' ')
                trainee_surgeon = TraineeSurgeon.objects.get(first_name=trainee_surgeon_names[1], last_name=trainee_surgeon_names[2])
                FavTraineeSurgeon.objects.create(surgeon=profile, trainee_surgeon=trainee_surgeon)
            for anesthesiologists in fav_team['anesthesiologists']:
                anesthesiologists_names = anesthesiologists.split(' ')
                anesthesiologists = Anesthesiologist.objects.get(first_name=anesthesiologists_names[1], last_name=anesthesiologists_names[2])
                FavAnesthesiologist.objects.create(surgeon=profile, anesthesiologist=anesthesiologists)
            for nurse in fav_team['nurse']:
                nurse_names = nurse.split(' ')
                nurse = Nurse.objects.get(first_name=nurse_names[1], last_name=nurse_names[2])
                FavNurse.objects.create(surgeon=profile, nurse=nurse)
            user_data['profile'] = user_profile_data
            return Response(user_data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def create_booked_team(request):
    if request.method == 'POST':
        print('CREATE TEAM -----------------------------------')
        request_data = JSONParser().parse(request)
        token = request_data['key']
        fav_team = request_data['favTeam']
        surgery_details = request_data['surgery_details']

        start_minute = surgery_details['start_minute']
        end_minute = surgery_details['end_minute']
        start_hour = surgery_details['start_hour']
        end_hour = surgery_details['end_hour']
        date = surgery_details['date']
        month = surgery_details['month']
        year = surgery_details['year']


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

            surgery = Surgery.objects.get(surgeon=profile,start_hour=start_hour,date=date,month=month,year=year)

            for trainee_surgeon in fav_team['trainee_surgeon']:
                trainee_surgeon_names = trainee_surgeon.split(' ')
                trainee_surgeon = TraineeSurgeon.objects.get(first_name=trainee_surgeon_names[1], last_name=trainee_surgeon_names[2])
                o = BookedTraineeSurgeon.objects.create(
                    surgery=surgery, trainee_surgeon=trainee_surgeon,start_minute=start_minute, start_hour=start_hour,
                    end_hour=end_hour, end_minute=end_minute, date=date, month=month, year=year
                )
                o.save()
            for anesthesiologists in fav_team['anesthesiologists']:
                anesthesiologists_names = anesthesiologists.split(' ')
                print(anesthesiologists_names)
                anesthesiologists = Anesthesiologist.objects.get(first_name=anesthesiologists_names[1], last_name=anesthesiologists_names[2])
                o = BookedAnesthesiologist.objects.create(
                    surgery=surgery, anesthesiologist=anesthesiologists,start_minute=start_minute, start_hour=start_hour,
                    end_hour=end_hour, end_minute=end_minute, date=date, month=month, year=year
                )
                o.save()
            for nurse in fav_team['nurse']:
                nurse_names = nurse.split(' ')
                nurse = Nurse.objects.get(first_name=nurse_names[1], last_name=nurse_names[2])
                o = BookedNurse.objects.create(
                    surgery=surgery, nurse=nurse,start_minute=start_minute, start_hour=start_hour,
                    end_hour=end_hour, end_minute=end_minute, date=date, month=month, year=year
                )
                o.save()
            user_data['profile'] = user_profile_data
            return Response(user_data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)
