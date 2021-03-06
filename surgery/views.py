from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from booked.models import BookedTraineeSurgeon, BookedNurse, BookedAnesthesiologist
from surgery.models import Surgery, Patient
from team.models import FavNurse, FavTraineeSurgeon, FavAnesthesiologist
from user.models import Surgeon, Nurse, TraineeSurgeon, Anesthesiologist
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import joblib
import calendar

@csrf_exempt
@api_view(['POST'])
def set_surgery_complete(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        id = request_data['id']

        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user
            surgeon = Surgeon.objects.get(user=user)
            Surgery.objects.filter(id = id).update(is_completed=True)
        return Response("valid", status=status.HTTP_200_OK, exception=False)




@csrf_exempt
@api_view(['POST'])
def get_surgeris(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user
            surgeon = Surgeon.objects.get(user=user)
            surgeries = []
            for surgery in Surgery.objects.filter(surgeon=surgeon):

                s = {
                        'id': surgery.id,
                        'Name': 'Knee Surgery',
                        'Time': get_time_text(surgery.start_hour, surgery.start_minute, surgery.end_hour,
                                                   surgery.end_minute),

                        'Day': calendar.month_abbr[surgery.month + 1] + " " + str(surgery.date),
                        'Completed': surgery.is_completed,

                    }
                if Patient.objects.filter(surgery=surgery).exists():
                    patient = Patient.objects.get(surgery=surgery)
                    s['patient_details'] = {
                            'patient_name': patient.first_name + ' ' + patient.last_name,
                            'email': patient.email,
                            'notes': patient.notes
                        }
                    surgeries.append(s)
                else:
                    s['patient_details'] = {}
                    surgeries.append(s)
            return Response(surgeries, status=status.HTTP_200_OK, exception=False)


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


@csrf_exempt
@api_view(['POST'])
def get_predicted_time(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            user = tObject.user
            surgeon_profile = Surgeon.objects.get(user=user)
            patient_details = request_data['patient_details']

            age = patient_details['age']
            gender = patient_details['gender']
            weight = patient_details['weight']
            height = patient_details['height']
            cancer = patient_details['cancer']
            cvd = patient_details['cvd']
            dementia = patient_details['dementia']
            diabetes = patient_details['diabetes']
            digestive = patient_details['digestive']
            osteoarthritis = patient_details['osteoarthritis']
            pylogical = patient_details['pylogical']
            pulmonary = patient_details['pulmonary']

            X = [[cancer, cvd, dementia, diabetes, digestive, osteoarthritis, pylogical, pulmonary]]
            predicted_result = duration_predict(age, X)
            time = predicted_result[0]

            hours = int(time)
            minutes = (time * 60) % 60
            seconds = (time * 3600) % 60

            data = {
                'time':time,
                'time_text': str(hours) + ' Hr  '+ str(int(minutes))+ ' Min'
            }

            return Response(data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


def duration_predict(age, X):
    model = joblib.load('static/random_forest_classifier_model.sav')
    stats_yes = joblib.load('static/stats_yes')
    stats_no = joblib.load('static/stats_no')

    complication = model.predict(X)[0]

    ranges = [(35, 40), (40, 45), (45, 50), (50, 55), (55, 60), (60, 65), (65, 70), (70, 75), (75, 80), (80, 85),
              (85, 90), (90, 95)]
    index = None

    for r in ranges:
        index = 0 if index == None else index + 1
        if r[0] <= age < r[1]:
            break

    if index >= 0:
        if complication == 1:
            return stats_yes[index]
        else:
            return stats_no[index]
    else:
        return None


@csrf_exempt
@api_view(['POST'])
def create_surgery_with_schedule(request):
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

            surgery = Surgery.objects.create(
                start_minute=surgery_details['start_minute'],
                end_minute=surgery_details['end_minute'],
                start_hour=surgery_details['start_hour'],
                end_hour=surgery_details['end_hour'],
                date=surgery_details['date'],
                month=surgery_details['month'],
                year=surgery_details['year'],
                predicted_time=surgery_details['predicted_time'],
                estimated_time=67,
                real_time=0,
                surgeon=surgeon_profile
            )
            surgery.save()
            patient = Patient.objects.create(
                first_name=patient_details['first_name'],
                last_name=patient_details['last_name'],
                address=patient_details['address'],
                email=patient_details['email'],
                telephone=patient_details['telephone'],
                notes=patient_details['note'],
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

            num_trainee_surgeon = 2
            num_anesthelogist = 2
            num_nurse = 5

            i = 0
            j = 0
            k = 0

            trainee_surgeons = []
            anesthelogist_list = []
            nurse = []

            date = surgery_details['date']
            month = surgery_details['month']
            year = surgery_details['year']
            start_hour = int(surgery_details['start_hour'])

            for t_surgeon in FavTraineeSurgeon.objects.filter(surgeon=surgeon_profile):
                print("Trainee Surgeon 01")
                if BookedTraineeSurgeon.objects.filter(trainee_surgeon=t_surgeon.trainee_surgeon, date=date,
                                                       month=month, year=year).exists():
                    if BookedTraineeSurgeon.objects.get(trainee_surgeon=t_surgeon.trainee_surgeon, date=date,
                                                        month=month, year=year).end_hour < start_hour:
                        if i < num_trainee_surgeon:
                            trainee_surgeons.append(
                                t_surgeon.trainee_surgeon.title + ' ' + t_surgeon.trainee_surgeon.first_name + ' ' + t_surgeon.trainee_surgeon.last_name)
                            i = i + 1
                        else:
                            break
                else:
                    if i < num_trainee_surgeon:
                        trainee_surgeons.append(
                            t_surgeon.trainee_surgeon.title + ' ' + t_surgeon.trainee_surgeon.first_name + ' ' + t_surgeon.trainee_surgeon.last_name)
                        i = i + 1
                    else:
                        break
            print("I valueeeeeeeeeeeeeeeeeeee")
            print(i)
            while i < num_trainee_surgeon:
                print("Trainee Surgeon 02")
                for t_surgeon in TraineeSurgeon.objects.all():
                    if BookedTraineeSurgeon.objects.filter(trainee_surgeon=t_surgeon, date=date,
                                                           month=month, year=year).exists():
                        if BookedTraineeSurgeon.objects.get(trainee_surgeon=t_surgeon, date=date,
                                                            month=month, year=year).end_hour < start_hour:
                            if i < num_trainee_surgeon:
                                if (
                                        t_surgeon.title + ' ' + t_surgeon.first_name + ' ' + t_surgeon.last_name) not in trainee_surgeons:
                                    trainee_surgeons.append(
                                        t_surgeon.title + ' ' + t_surgeon.first_name + ' ' + t_surgeon.last_name)
                                    i = i + 1
                            else:
                                break
                    else:
                        if i < num_trainee_surgeon:
                            if (
                                    t_surgeon.title + ' ' + t_surgeon.first_name + ' ' + t_surgeon.last_name) not in trainee_surgeons:
                                trainee_surgeons.append(
                                    t_surgeon.title + ' ' + t_surgeon.first_name + ' ' + t_surgeon.last_name)
                                i = i + 1
                        else:
                            break

            # Get fav Nurse
            for t_nurse in FavNurse.objects.filter(surgeon=surgeon_profile):
                print("Nurse 01")
                if BookedNurse.objects.filter(nurse=t_nurse.nurse, date=date, month=month, year=year).exists():
                    if BookedNurse.objects.get(nurse=t_nurse.nurse, date=date, month=month,
                                               year=year).end_hour < start_hour:
                        if i < num_nurse:
                            nurse.append(
                                t_nurse.nurse.title + ' ' + t_nurse.nurse.first_name + ' ' + t_nurse.nurse.last_name)
                            j = j + 1
                        else:
                            break
                else:
                    if j < num_nurse:
                        nurse.append(
                            t_nurse.nurse.title + ' ' + t_nurse.nurse.first_name + ' ' + t_nurse.nurse.last_name)
                        j = j + 1
                    else:
                        break

            while j < num_nurse:
                print("Nurse 02")
                for t_nurse in Nurse.objects.all():
                    if BookedNurse.objects.filter(nurse=t_nurse, date=date,
                                                  month=month, year=year).exists():
                        if BookedNurse.objects.get(trainee_surgeon=t_nurse, date=date,
                                                   month=month, year=year).end_hour < start_hour:
                            if i < num_nurse:
                                if (t_nurse.title + ' ' + t_nurse.first_name + ' ' + t_nurse.last_name) not in nurse:
                                    nurse.append(
                                        t_nurse.title + ' ' + t_nurse.first_name + ' ' + t_nurse.last_name)
                                    j = j + 1
                            else:
                                break
                    else:
                        if j < num_nurse:
                            if (
                                    t_nurse.title + ' ' + t_nurse.first_name + ' ' + t_nurse.last_name) not in nurse:
                                nurse.append(
                                    t_nurse.title + ' ' + t_nurse.first_name + ' ' + t_nurse.last_name)
                                j = j + 1
                        else:
                            break

            # Anesthelogist
            for t_anesth in FavAnesthesiologist.objects.filter(surgeon=surgeon_profile):
                print("Anesthelogist 01")

                if BookedAnesthesiologist.objects.filter(anesthesiologist=t_anesth.anesthesiologist, date=date,
                                                         month=month, year=year).exists():
                    if BookedAnesthesiologist.objects.get(anesthesiologist=t_anesth.anesthesiologist, date=date,
                                                          month=month, year=year).end_hour < start_hour:
                        if k < num_anesthelogist:

                            anesthelogist_list.append(
                                t_anesth.anesthesiologist.title + ' ' + t_anesth.anesthesiologist.first_name + ' ' + t_anesth.anesthesiologist.last_name)
                            k = k + 1
                        else:
                            break
                else:
                    if k < num_anesthelogist:
                        anesthelogist_list.append(
                            t_anesth.anesthesiologist.title + ' ' + t_anesth.anesthesiologist.first_name + ' ' + t_anesth.anesthesiologist.last_name)
                        k = k + 1
                    else:
                        break

            while k < num_anesthelogist:
                print("Anesthelogist 02")

                for t_anesth in Anesthesiologist.objects.all():
                    if BookedAnesthesiologist.objects.filter(anesthesiologist=t_anesth, date=date,
                                                             month=month, year=year).exists():
                        if BookedAnesthesiologist.objects.get(anesthesiologist=t_anesth, date=date,
                                                              month=month, year=year).end_hour < start_hour:
                            if k < num_anesthelogist:
                                if (
                                        t_anesth.title + ' ' + t_anesth.first_name + ' ' + t_anesth.last_name) not in anesthelogist_list:
                                    anesthelogist_list.append(
                                        t_anesth.title + ' ' + t_anesth.first_name + ' ' + t_anesth.last_name)
                                    k = k + 1
                            else:
                                break
                    else:
                        if k < num_anesthelogist:
                            if (
                                    t_anesth.title + ' ' + t_anesth.first_name + ' ' + t_anesth.last_name) not in anesthelogist_list:
                                anesthelogist_list.append(
                                    t_anesth.title + ' ' + t_anesth.first_name + ' ' + t_anesth.last_name)
                                k = k + 1
                        else:
                            break

            all_nurse = []
            all_trainee_surgeon = []
            all_anesthesiologist = []

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
                'fav_nurse': nurse,
                'fav_trainee_surgeon': trainee_surgeons,
                'fav_anesthesiologist': anesthelogist_list
            }

            print('///// ------ alL team details ------- /////////')
            print(all)
            print('//////////////////////////////////////////////////////')
            print("888888888888888888888888888888888888888888888")

            return Response(all, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)
