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
def get_predicted_time(request):
    pass



@csrf_exempt
@api_view(['POST'])
def create_surgery(request):
    if request.method == 'POST':
        print('CREATE TEAM ///////////////////////////////////')
        request_data = JSONParser().parse(request)
        token = request_data['key']
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

            user_data['profile'] = user_profile_data
            return Response(user_data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)
