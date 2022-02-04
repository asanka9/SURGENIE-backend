from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from hospital.models import Resource
from team.models import FavNurse, FavTraineeSurgeon, FavAnesthesiologist
from user.models import Surgeon, Nurse, TraineeSurgeon, Anesthesiologist, Admin
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@csrf_exempt
@api_view(['POST'])
def add_resource(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            resource = request_data['resource']
            Resource.objects.create(name=resource['name'], amount=resource['amount'], availability=True,
                                    unit=resource['unit'])
            print('Resource Added Successfully')
            return Response('valid', status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def view_resources(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            tObject = Token.objects.get(key=token)
            resources = []
            for resource in Resource.objects.all():
                resources.append({'name': resource.name, 'amount': resource.amount, 'id': resource.id,
                                  'availability': resource.availability})

            return Response(resources, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def all_nurse(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            users = []
            for i in Nurse.objects.all():
                users.append({
                    'name': i.title + ' ' + i.first_name + ' ' + i.last_name,
                    'email': i.email,
                    'telephone': i.telephone,
                    'id': i.id
                })
            return Response(users, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def all_anesthesiologist(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            users = []
            for i in Anesthesiologist.objects.all():
                users.append({
                    'name': i.title + ' ' + i.first_name + ' ' + i.last_name,
                    'email': i.email,
                    'telephone': i.telephone,
                    'id': i.id
                })
            return Response(users, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def all_surgeon(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            users = []
            for i in Surgeon.objects.all():
                users.append({
                    'name': i.title + ' ' + i.first_name + ' ' + i.last_name,
                    'email': i.email,
                    'telephone': i.telephone,
                    'id': i.id
                })
            return Response(users, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def all_admin(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            users = []
            for i in Admin.objects.all():
                users.append({
                    'name': i.title + ' ' + i.first_name + ' ' + i.last_name,
                    'email': i.email,
                    'telephone': i.telephone,
                    'id': i.id
                })
            return Response(users, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def all_trainee_surgeon(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        if Token.objects.filter(key=token).exists():
            users = []
            for i in TraineeSurgeon.objects.all():
                users.append({
                    'name': i.title + ' ' + i.first_name + ' ' + i.last_name,
                    'email': i.email,
                    'telephone': i.telephone,
                    'id': i.id
                })
            return Response(users, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)