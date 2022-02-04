from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from team.models import FavNurse, FavTraineeSurgeon, FavAnesthesiologist
from user.models import Surgeon, Nurse, TraineeSurgeon, Anesthesiologist
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@csrf_exempt
@api_view(['POST'])
def get_booked_detail_date(request):
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
def get_booked_detail_date_range(request):
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
