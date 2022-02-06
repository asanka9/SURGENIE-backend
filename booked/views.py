from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from booked.models import BookedNurse, BookedAnesthesiologist, BookedTraineeSurgeon
from surgery.models import Surgery, Patient
from team.models import FavNurse, FavTraineeSurgeon, FavAnesthesiologist
from user.models import Surgeon, Nurse, TraineeSurgeon, Anesthesiologist, Admin
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@csrf_exempt
@api_view(['POST'])
def get_booked_detail_date_range(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        start_day = request_data['start_day']
        end_day = request_data['end_day']

        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user

            start_date = start_day['date']
            start_month = start_day['month']
            start_year = start_day['year']

            end_date = end_day['date']
            end_month = end_day['month']
            end_year = end_day['year']

            admin_data = []
            nurse_data = []
            surgeon_data = []
            trainee_surgeon_data = []
            anesthesiologist_data = []

            if user.is_admin_staff:
                if start_month != end_month:
                    for m in range(start_month, end_month):
                        for d in range(start_date, end_date):

                            for surgery in Surgery.objects.filter(date=d, month=m, year=2022):
                                patient = Patient.objects.get(surgery=surgery)
                                patient_detail = {
                                    'patient_name': patient.first_name + ' ' + patient.last_name,
                                    'email': patient.email,
                                    'telephone': patient.telephone
                                }

                                admin_data.append({
                                    'start_hour': surgery.start_hour,
                                    'start-minute': surgery.start_minute,
                                    'end_hour': surgery.end_hour,
                                    'end_minute': surgery.end_minute,
                                    'time_text': get_time_text(start_hour=surgery.start_hour,
                                                               start_minute=surgery.start_minute,
                                                               end_hour=surgery.end_hour,
                                                               end_minute=surgery.end_minute),
                                    'patient_detail': patient_detail
                                })
                    return Response({'user': 'admin', 'data': admin_data}, status=status.HTTP_200_OK, exception=False)
                else:
                    for d in range(start_date, end_date):

                        for surgery in Surgery.objects.filter(date=d, month=start_month, year=2022):
                            patient = Patient.objects.get(surgery=surgery)
                            patient_detail = {
                                'patient_name': patient.first_name + ' ' + patient.last_name,
                                'email': patient.email,
                                'telephone': patient.telephone
                            }

                            admin_data.append({
                                'start_hour': surgery.start_hour,
                                'start-minute': surgery.start_minute,
                                'end_hour': surgery.end_hour,
                                'end_minute': surgery.end_minute,
                                'time_text': get_time_text(start_hour=surgery.start_hour,
                                                           start_minute=surgery.start_minute,
                                                           end_hour=surgery.end_hour,
                                                           end_minute=surgery.end_minute),
                                'patient_detail': patient_detail
                            })
                    return Response({'user': 'admin', 'data': admin_data}, status=status.HTTP_200_OK, exception=False)
            elif user.is_medical_staff:
                if user.role == 'surgeon':
                    if start_month != end_month:
                        for m in range(start_month, end_month):
                            for d in range(start_date, end_date):
                                surgeon = Surgeon.objects.get(user=user)
                                for b in Surgery.objects.filter(surgeon=surgeon, date=d, month=m, year=2022):
                                    patient_detail = {}
                                    if Patient.objects.filter(surgery=b).exists():
                                        patient = Patient.objects.get(surgery=b)
                                        patient_detail = {
                                            'patient_name': patient.first_name + ' ' + patient.last_name,
                                            'email': patient.email,
                                            'telephone': patient.telephone,
                                            'notes': patient.notes
                                        }

                                    surgeon_data.append(
                                        {
                                            'start_hour': b.start_hour,
                                            'start-minute': b.start_minute,
                                            'end_hour': b.end_hour,
                                            'end_minute': b.end_minute,
                                            'time_text': get_time_text(start_hour=b.start_hour,
                                                                       start_minute=b.start_minute,
                                                                       end_hour=b.end_hour, end_minute=b.end_minute),
                                            'patient_details': patient_detail
                                        }
                                    )
                        return Response({'user': 'surgeon', 'data': surgeon_data}, status=status.HTTP_200_OK,
                                                exception=False)
                    else:
                        for d in range(start_date, end_date):
                            surgeon = Surgeon.objects.get(user=user)
                            for b in Surgery.objects.filter(surgeon=surgeon, date=d, month=start_month, year=2022):
                                patient_detail = {}
                                if Patient.objects.filter(surgery=b).exists():
                                    patient = Patient.objects.get(surgery=b)
                                    patient_detail = {
                                        'patient_name': patient.first_name + ' ' + patient.last_name,
                                        'email': patient.email,
                                        'telephone': patient.telephone,
                                        'notes': patient.notes
                                    }

                                surgeon_data.append(
                                    {
                                        'start_hour': b.start_hour,
                                        'start-minute': b.start_minute,
                                        'end_hour': b.end_hour,
                                        'end_minute': b.end_minute,
                                        'time_text': get_time_text(start_hour=b.start_hour, start_minute=b.start_minute,
                                                                   end_hour=b.end_hour, end_minute=b.end_minute),
                                        'patient_details': patient_detail
                                    }
                                )
                        return Response({'user': 'surgeon', 'data': surgeon_data}, status=status.HTTP_200_OK,
                                            exception=False)

                if user.role == 'nurse':
                    if start_month != end_month:
                        for m in range(start_month, end_month):
                            for d in range(start_date, end_date):
                                nurse = Nurse.objects.get(user=user)
                                for b in BookedNurse.objects.filter(nurse=nurse, date=d, month=m, year=2022):
                                    nurse_data.append(
                                        {
                                            'start_hour': b.start_hour,
                                            'start-minute': b.start_minute,
                                            'end_hour': b.end_hour,
                                            'end_minute': b.end_minute,
                                            'time_text': get_time_text(start_hour=b.start_hour,
                                                                       start_minute=b.start_minute,
                                                                       end_hour=b.end_hour, end_minute=b.end_minute),
                                            'surgeon_name': 'Dr ' + b.surgery.surgeon.first_name + ' ' + b.surgery.surgeon.last_name
                                        }
                                    )
                        return Response({'user': 'nurse', 'data': nurse_data}, status=status.HTTP_200_OK,
                                                exception=False)
                    else:
                        for d in range(start_date, end_date):
                            nurse = Nurse.objects.get(user=user)
                            for b in BookedNurse.objects.filter(nurse=nurse, date=d, month=start_month, year=2022):
                                nurse_data.append(
                                    {
                                        'start_hour': b.start_hour,
                                        'start-minute': b.start_minute,
                                        'end_hour': b.end_hour,
                                        'end_minute': b.end_minute,
                                        'time_text': get_time_text(start_hour=b.start_hour, start_minute=b.start_minute,
                                                                   end_hour=b.end_hour, end_minute=b.end_minute),
                                        'surgeon_name': 'Dr ' + b.surgery.surgeon.first_name + ' ' + b.surgery.surgeon.last_name
                                    }
                                )
                            return Response({'user': 'nurse', 'data': nurse_data}, status=status.HTTP_200_OK,
                                            exception=False)

                if user.role == 'trainee_surgeon':
                    if start_month != end_month:
                        for m in range(start_month, end_month):
                            for d in range(start_date, end_date):
                                trainee_surgeon = TraineeSurgeon.objects.get(user=user)
                                for b in BookedTraineeSurgeon.objects.filter(trainee_surgeon=trainee_surgeon, date=d,
                                                                             month=m, year=2022):
                                    trainee_surgeon_data.append(
                                        {
                                            'start_hour': b.start_hour,
                                            'start-minute': b.start_minute,
                                            'end_hour': b.end_hour,
                                            'end_minute': b.end_minute,
                                            'time_text': get_time_text(start_hour=b.start_hour,
                                                                       start_minute=b.start_minute,
                                                                       end_hour=b.end_hour, end_minute=b.end_minute),
                                            'surgeon_name': 'Dr ' + b.surgery.surgeon.first_name + ' ' + b.surgery.surgeon.last_name
                                        }
                                    )
                        return Response({'user': 'trainee_surgeon', 'data': trainee_surgeon_data},
                                                status=status.HTTP_200_OK, exception=False)
                    else:
                        for d in range(start_date, end_date):
                            trainee_surgeon = TraineeSurgeon.objects.get(user=user)
                            for b in BookedTraineeSurgeon.objects.filter(trainee_surgeon=trainee_surgeon, date=d,
                                                                         month=start_month, year=2022):
                                trainee_surgeon_data.append(
                                    {
                                        'start_hour': b.start_hour,
                                        'start-minute': b.start_minute,
                                        'end_hour': b.end_hour,
                                        'end_minute': b.end_minute,
                                        'time_text': get_time_text(start_hour=b.start_hour, start_minute=b.start_minute,
                                                                   end_hour=b.end_hour, end_minute=b.end_minute),
                                        'surgeon_name': 'Dr ' + b.surgery.surgeon.first_name + ' ' + b.surgery.surgeon.last_name
                                    }
                                )
                        return Response({'user': 'trainee_surgeon', 'data': trainee_surgeon_data},
                                            status=status.HTTP_200_OK, exception=False)

                if user.role == 'anesthesiologist':
                    if start_month != end_month:
                        for m in range(start_month, end_month):
                            for d in range(start_date, end_date):
                                anesthesiologist = Anesthesiologist.objects.get(user=user)
                                for b in BookedAnesthesiologist.objects.filter(anesthesiologist=anesthesiologist,
                                                                               date=d,
                                                                               month=m, year=2022):
                                    anesthesiologist_data.append(
                                        {
                                            'start_hour': b.start_hour,
                                            'start-minute': b.start_minute,
                                            'end_hour': b.end_hour,
                                            'end_minute': b.end_minute,
                                            'time_text': get_time_text(start_hour=b.start_hour,
                                                                       start_minute=b.start_minute,
                                                                       end_hour=b.end_hour, end_minute=b.end_minute),
                                            'surgeon_name': 'Dr ' + b.surgery.surgeon.first_name + ' ' + b.surgery.surgeon.last_name
                                        }
                                    )
                        return Response({'user': 'anesthesiologist', 'data': anesthesiologist_data},
                                                status=status.HTTP_200_OK, exception=False)
                    else:
                        for d in range(start_date, end_date):
                            anesthesiologist = Anesthesiologist.objects.get(user=user)
                            for b in BookedAnesthesiologist.objects.filter(anesthesiologist=anesthesiologist, date=d,
                                                                           month=start_month, year=2022):
                                anesthesiologist_data.append(
                                    {
                                        'start_hour': b.start_hour,
                                        'start-minute': b.start_minute,
                                        'end_hour': b.end_hour,
                                        'end_minute': b.end_minute,
                                        'time_text': get_time_text(start_hour=b.start_hour, start_minute=b.start_minute,
                                                                   end_hour=b.end_hour, end_minute=b.end_minute),
                                        'surgeon_name': 'Dr ' + b.surgery.surgeon.first_name + ' ' + b.surgery.surgeon.last_name
                                    }
                                )
                        return Response({'user': 'anesthesiologist', 'data': anesthesiologist_data},
                                            status=status.HTTP_200_OK, exception=False)


@csrf_exempt
@api_view(['POST'])
def get_booked_detail_date(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        day = request_data['day']

        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user

            date = day['date']
            month = day['month']
            year = day['year']

            admin_data = []
            nurse_data = []
            surgeon_data = []
            trainee_surgeon_data = []
            anesthesiologist_data = []

            if user.is_admin_staff:
                print('CAll here')
                for surgery in Surgery.objects.filter(date=date, month=month, year=year):
                    # patient = Patient.objects.get(surgery=surgery)
                    # patient_detail = {
                    #     'patient_name': patient.first_name + ' ' + patient.last_name,
                    #     'email': patient.email,
                    #     'telephone': patient.telephone
                    # }

                    admin_data.append({
                        'start_hour': surgery.start_hour,
                        'start-minute': surgery.start_minute,
                        'end_hour': surgery.end_hour,
                        'end_minute': surgery.end_minute,
                        'time_text': get_time_text(start_hour=surgery.start_hour, start_minute=surgery.start_minute,
                                                   end_hour=surgery.end_hour, end_minute=surgery.end_minute),
                        'patient_detail': {}
                    })
                print(admin_data)
                return Response({'user': 'admin', 'data': admin_data}, status=status.HTTP_200_OK, exception=False)
            elif user.is_medical_staff:
                if user.role == 'surgeon':
                    surgeon = Surgeon.objects.get(user=user)
                    for b in Surgery.objects.filter(surgeon=surgeon, date=date, month=month, year=year):
                        patient = Patient.objects.get(surgery=b)
                        patient_detail = {
                            'patient_name': patient.first_name + ' ' + patient.last_name,
                            'email': patient.email,
                            'telephone': patient.telephone,
                            'notes': patient.notes
                        }
                        surgeon_data.append(
                            {
                                'start_hour': b.start_hour,
                                'start-minute': b.start_minute,
                                'end_hour': b.end_hour,
                                'end_minute': b.end_minute,
                                'time_text': get_time_text(start_hour=b.start_hour, start_minute=b.start_minute,
                                                           end_hour=b.end_hour, end_minute=b.end_minute),
                                'patient_details': patient_detail
                            }
                        )
                    return Response({'user': 'surgeon', 'data': surgeon_data}, status=status.HTTP_200_OK,
                                    exception=False)
                elif user.role == 'nurse':
                    nurse = Nurse.objects.get(user=user)
                    for b in BookedNurse.objects.filter(nurse=nurse, date=date, month=month, year=year):
                        nurse_data.append(
                            {
                                'start_hour': b.start_hour,
                                'start-minute': b.start_minute,
                                'end_hour': b.end_hour,
                                'end_minute': b.end_minute,
                                'time_text': get_time_text(start_hour=b.start_hour, start_minute=b.start_minute,
                                                           end_hour=b.end_hour, end_minute=b.end_minute),
                                'surgeon_name': 'Dr ' + b.surgery.surgeon.first_name + ' ' + b.surgery.surgeon.last_name
                            }
                        )
                    return Response({'user': 'nurse', 'data': nurse_data}, status=status.HTTP_200_OK, exception=False)
                elif user.role == 'trainee_surgeon':
                    trainee_surgeon = TraineeSurgeon.objects.get(user=user)
                    for b in BookedTraineeSurgeon.objects.filter(trainee_surgeon=trainee_surgeon, date=date,
                                                                 month=month, year=year):
                        trainee_surgeon_data.append(
                            {
                                'start_hour': b.start_hour,
                                'start-minute': b.start_minute,
                                'end_hour': b.end_hour,
                                'end_minute': b.end_minute,
                                'time_text': get_time_text(start_hour=b.start_hour, start_minute=b.start_minute,
                                                           end_hour=b.end_hour, end_minute=b.end_minute),
                                'surgeon_name': 'Dr ' + b.surgery.surgeon.first_name + ' ' + b.surgery.surgeon.last_name
                            }
                        )
                    return Response({'user': 'trainee_surgeon', 'data': trainee_surgeon_data},
                                    status=status.HTTP_200_OK, exception=False)
                elif user.role == 'anesthesiologist':
                    anesthesiologist = Anesthesiologist.objects.get(user=user)
                    for b in BookedAnesthesiologist.objects.filter(anesthesiologist=anesthesiologist, date=date,
                                                                   month=month, year=year):
                        anesthesiologist_data.append(
                            {
                                'start_hour': b.start_hour,
                                'start-minute': b.start_minute,
                                'end_hour': b.end_hour,
                                'end_minute': b.end_minute,
                                'time_text': get_time_text(start_hour=b.start_hour, start_minute=b.start_minute,
                                                           end_hour=b.end_hour, end_minute=b.end_minute),
                                'surgeon_name': 'Dr ' + b.surgery.surgeon.first_name + ' ' + b.surgery.surgeon.last_name
                            }
                        )
                    return Response({'user': 'anesthesiologist', 'data': anesthesiologist_data},
                                    status=status.HTTP_200_OK, exception=False)


def get_time_text(start_hour, start_minute, end_hour, end_minute):
    text_1 = ''
    text_2 = ''

    if start_hour <= 12:
        text_1 = str(start_hour) + " : " + str(start_minute) + " AM"
    else:
        text_1 = str(start_hour - 12) + " : " + str(start_minute) + " PM"

    if end_hour <= 12:
        text_2 = str(end_hour) + " : " + str(end_minute) + " AM"
    else:
        text_2 = str(end_hour - 12) + " : " + str(end_minute) + " PM"

    return text_1 + " - " + text_2





@csrf_exempt
@api_view(['POST'])
def get_booked_surgery_history(request):
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
def get_calender_with_date(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user


@csrf_exempt
@api_view(['POST'])
def get_calender_with_date_range(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user


@csrf_exempt
@api_view(['POST'])
def add_book(request):
    pass
