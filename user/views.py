from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, renderer_classes

from rest_framework import status

from user.models import Account, Nurse, Surgeon, SurgeonSession, TraineeSurgeon, TraineeSurgeonSession, \
    Anesthesiologist, Admin


class ProfileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user.email),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print("Login Request is Coming ==========")
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # profile = BlogProfile.objects.get(user=user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            # 'profile_url': profile.profile_url
        }, status=status.HTTP_200_OK, exception=False)


@csrf_exempt
@api_view(['POST'])
def verify_token(request):
    if request.method == 'POST':
        # print(JSONParser().parse(request)['key'])
        # print(Token.objects.filter(KEY = JSONParser().parse(request)['key']))
        token = JSONParser().parse(request)['key']
        if (Token.objects.filter(key=token).exists()):
            tObject = Token.objects.get(key=token)
            user = tObject.user
            # profile = BlogProfile.objects.get(user=user)
            # blogs = Blog.objects.all().filter(blog_profile=profile)

            # blog_list = []
            # for blog in blogs:
            #     blog_map = {}
            #     blog_map['blog_url'] = blog.blog_url
            #     blog_map['blog_name'] = blog.blog_name
            #     """
            #     posts = Post.objects.all().filter(blog=blog)
            #     post_list = []
            #     for post in posts:
            #         post_map = {}
            #         post_map['title'] = post.title
            #         post_map['position'] = post.position
            #         post_map['youtube_id'] = post.youtube_id
            #         post_map['inner_html'] = post.inner_html
            #         post_list.append(post_map)
            #     blog_map['post_list'] = post_list
            #     """
            #     blog_list.append(blog_map)

            # is_medical_staff = models.BooleanField(default=False, null=True)
            # is_admin_staff = models.BooleanField(default=False, null=True)
            # role = models.CharField(max_length=20, choices=ROLES, null=True)
            #

            user_data = {
                'user_id': user.pk,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_medical_staff': user.is_medical_staff,
                'is_admin_staff': user.is_admin_staff,
                'role': user.role
                # 'profile_url': profile.profile_url,
                # 'blog_list': blog_list
            }

            return Response(user_data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def userInfo(request):
    if request.method == 'POST':
        token = JSONParser().parse(request)['key']
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
            if user.is_admin_staff:
                profile = Admin.objects.get(user=user)
                user_profile_data['title'] = profile.title
                user_profile_data['first_name'] = profile.first_name
                user_profile_data['last_name'] = profile.last_name
                user_profile_data['address'] = profile.address
                user_profile_data['email'] = profile.email
                user_profile_data['telephone'] = profile.telephone
                user_profile_data['level'] = 'admin-0' + str(profile.level)
            elif user.is_medical_staff:
                if user.role == 'anesthesiologist':
                    profile = Anesthesiologist.objects.get(user=user)
                    user_profile_data['title'] = profile.title
                    user_profile_data['first_name'] = profile.first_name
                    user_profile_data['last_name'] = profile.last_name
                    user_profile_data['address'] = profile.address
                    user_profile_data['email'] = profile.email
                    user_profile_data['registration_number'] = profile.email
                if user.role == 'surgeon':
                    profile = Surgeon.objects.get(user=user)
                    user_profile_data['title'] = profile.title
                    user_profile_data['first_name'] = profile.first_name
                    user_profile_data['last_name'] = profile.last_name
                    user_profile_data['address'] = profile.address
                    user_profile_data['email'] = profile.email
                    user_profile_data['telephone'] = profile.telephone
                    user_profile_data['registration_number'] = profile.registration_number
                if user.role == 'trainee_surgeon':
                    profile = TraineeSurgeon.objects.get(user=user)
                    user_profile_data['title'] = profile.title
                    user_profile_data['first_name'] = profile.first_name
                    user_profile_data['last_name'] = profile.last_name
                    user_profile_data['address'] = profile.address
                    user_profile_data['email'] = profile.email
                    user_profile_data['registration_number'] = profile.email
                if user.role == 'nurse':
                    profile = Nurse.objects.get(user=user)
                    user_profile_data['title'] = profile.title
                    user_profile_data['first_name'] = profile.first_name
                    user_profile_data['last_name'] = profile.last_name
                    user_profile_data['address'] = profile.address
                    user_profile_data['email'] = profile.email
                    user_profile_data['registration_number'] = profile.email
            user_data['profile'] = user_profile_data
            return Response(user_data, status=status.HTTP_200_OK, exception=False)
        else:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        print("Register User is Callling")
        account = JSONParser().parse(request)
        print(account)
        account['username'] = account['email']
        try:
            title = account['title']
            email = account['email']
            first_name = account['first_name']
            last_name = account['last_name']
            is_admin_staff = account['is_admin_staff']
            is_medical_staff = account['is_medical_staff']
            role = account['role']
            username = account['username']
            address = account['address']
            telephone = account['telephone']
            user = Account.objects.create_user(email=email, first_name=first_name,
                                               last_name=last_name,
                                               is_admin_staff=is_admin_staff, is_medical_staff=is_medical_staff,
                                               role=role,
                                               username=username, password='123456')

            if is_medical_staff:
                if role == 'nurse':
                    profile = Nurse.objects.create(
                        title=title,
                        user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                        registration_number=account['registration_number'],
                        is_sister=account['is_sister'], telephone=telephone
                    )
                    profile.save()
                elif role == 'anesthesiologist':
                    profile = Anesthesiologist.objects.create(
                        title=title,
                        user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                        registration_number=account['registration_number'], telephone=telephone
                    )
                    profile.save()
                elif role == 'trainee_surgeon':
                    print("Trainee Surgeon is Calling ==========================")
                    profile = TraineeSurgeon.objects.create(
                        title=title,
                        user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                        registration_number=account['registration_number'], specialty=account['specialty'],
                        telephone=telephone
                    )
                    profile.save()
                    for session in account['session']:
                        times = session['session'].split('-')
                        day = session['day']
                        session_object = TraineeSurgeonSession.objects.create(
                            trainee_surgeon=profile,
                            day=day, start_time=times[0], end_time=times[1]
                        )
                        session_object.save()
                elif role == 'surgeon':
                    profile = Surgeon.objects.create(
                        title=title,
                        user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                        registration_number=account['registration_number'], specialty=account['specialty'],
                        telephone=telephone
                    )
                    profile.save()
                    for session in account['session']:
                        times = session['session'].split('-')
                        day = session['day']
                        session_object = SurgeonSession.objects.create(
                            surgeon=profile,
                            day=day, start_time=times[0], end_time=times[1]
                        )
                        session_object.save()
            elif is_admin_staff:
                if role == 'admin-01':
                    profile = Admin.objects.create(
                        title=title,
                        user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                        level=1, telephone=telephone
                    )
                    profile.save()
                if role == 'admin-02':
                    profile = Admin.objects.create(
                        title=title,
                        user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                        level=2, telephone=telephone
                    )
                    profile.save()
                if role == 'admin-03':
                    profile = Admin.objects.create(
                        title=title,
                        user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                        level=3, telephone=telephone
                    )
                    profile.save()
                if role == 'admin-04':
                    profile = Admin.objects.create(
                        title=title,
                        user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                        level=4, telephone=telephone
                    )
                    profile.save()
                if role == 'admin-05':
                    profile = Admin.objects.create(
                        title=title,
                        user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                        level=5, telephone=telephone
                    )
                    profile.save()
            user.save()
            return Response('valid', status=status.HTTP_200_OK, exception=False)
        except Exception as e:
            print(e)
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)


@csrf_exempt
@api_view(['POST'])
def updateUser(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        token = request_data['key']
        account = request_data['user']

        if (Token.objects.filter(key=token).exists()):
            tObject = Token.objects.get(key=token)
            user = tObject.user
            try:
                title = account['title']
                email = account['email']
                first_name = account['first_name']
                last_name = account['last_name']
                address = account['address']
                telephone = account['telephone']
                print('helloooooooooooooooooooooooooooo')
                print(user.role)
                if user.is_medical_staff:
                    if user.role == 'nurse':
                        Nurse.objects.filter(user=user).update(
                            title=title,
                            user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                            registration_number=account['registration_number'],
                            is_sister=account['is_sister'], telephone=telephone
                        )
                    elif user.role == 'anesthesiologist':
                        Anesthesiologist.objects.filter(user=user).update(
                            title=title,
                            user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                            registration_number=account['registration_number'], telephone=telephone
                        )
                    elif user.role == 'trainee_surgeon':
                        TraineeSurgeon.objects.filter(user=user).update(
                            title=title,
                            user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                            registration_number=account['registration_number'], specialty=account['specialty'],
                            telephone=telephone
                        )
                        profile = TraineeSurgeon.objects.get(user=user)
                        TraineeSurgeonSession.objects.filter(surgeon=profile).delete()
                        for session in account['session']:
                            times = session['session'].split('-')
                            day = session['day']
                            session_object = TraineeSurgeonSession.objects.create(
                                trainee_surgeon=profile,
                                day=day, start_time=times[0], end_time=times[1]
                            )
                            session_object.save()
                    elif user.role == 'surgeon':
                        Surgeon.objects.filter(user=user).update(
                            title=title,
                            user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                            registration_number=account['registration_number'], specialty=account['specialty'],
                            telephone=telephone
                        )
                        profile = Surgeon.objects.get(user=user)
                        SurgeonSession.objects.filter(surgeon=profile).delete()
                        for session in account['session']:
                            times = session['session'].split('-')
                            day = session['day']
                            session_object = SurgeonSession.objects.create(
                                surgeon=profile,
                                day=day, start_time=times[0], end_time=times[1]
                            )
                            session_object.save()
                elif user.is_admin_staff:
                    if user.role == 'admin-01':
                        Admin.objects.filter(user=user).update(
                            title=title,
                            user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                            level=1, telephone=telephone
                        )
                    if user.role == 'admin-02':
                        Admin.objects.filter(user=user).update(
                            title=title,
                            user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                            level=2, telephone=telephone
                        )
                    if user.role == 'admin-03':
                        Admin.objects.filter(user=user).update(
                            title=title,
                            first_name=first_name, last_name=last_name, email=email, address=address,
                            level=3, telephone=telephone
                        )
                    if user.role == 'admin-04':
                        Admin.objects.filter(user=user).update(
                            title=title,
                            user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                            level=4, telephone=telephone
                        )
                    if user.role == 'admin-05':
                        Admin.objects.filter(user=user).update(
                            title=title,
                            user=user, first_name=first_name, last_name=last_name, email=email, address=address,
                            level=5, telephone=telephone
                        )
                return Response('valid', status=status.HTTP_200_OK, exception=False)
            except Exception as e:
                print(e)
                return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)













@csrf_exempt
@api_view(['GET'])
def get_all_medical_staff(request):
    token = JSONParser().parse(request)['key']
    if (Token.objects.filter(key=token).exists()):
        tObject = Token.objects.get(key=token)
        user = tObject.user

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
            'anesthesiologist': all_anesthesiologist
        }

        return Response(all, status=status.HTTP_200_OK, exception=False)


@csrf_exempt
@api_view(['DELETE'])
def logout(request):
    if request.method == 'DELETE':
        account = JSONParser().parse(request)
        account['username'] = account['email']
        try:
            user = User.objects.create_user(email=account['email'], first_name=account['first_name'],
                                            last_name=account['last_name'],
                                            username=account['username'], password=account['password'])
            # profile = BlogProfile.objects.create(user=user, profile_url=account['profile_url'])
            # profile.save()
            user.save()
            return Response('valid', status=status.HTTP_200_OK, exception=False)
        except Exception as e:
            return Response('invalid', status=status.HTTP_400_BAD_REQUEST, exception=True)
