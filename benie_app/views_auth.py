from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from benie_app import serializers_auth
from benie_app.renderers import UserJSONRenderer
from benie_app.models import MyUser
from benie_app.serializers_auth import ChangePasswordSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, UpdateSerializer, UserSerializer
import datetime
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.core.mail import send_mail
from django.http import Http404
import os
import sendgrid
from sendgrid.helpers.mail import *
from decouple import config 

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAdminUser

from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from benie_app.models import MyUser as User
from benie_app import utils
from knox.models import AuthToken
from django.urls import reverse


from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
# from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# from .utils import Util
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
from django.template.loader import render_to_string
import random
from datetime import timedelta
from django.conf import settings
from django.utils import timezone

from rest_framework import parsers, renderers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from benie_app.tokens import account_activation_token
# Create your views here.'

@permission_classes([IsAdminUser,])
class AllAdmins(APIView):
    def get_all_profiles(self):
        try:
            return MyUser.objects.all().filter(is_staff=True)
        except MyUser.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        profiles = MyUser.objects.all().filter(is_staff=True)
        serializers = UserSerializer(profiles,many=True)
        return Response(serializers.data)

@permission_classes([IsAdminUser,])
class UserProfiles(APIView):
    def get_all_users(self):
        try:
            return MyUser.objects.all()
        except MyUser.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        user_profiles = MyUser.objects.all()
        serializers = UserSerializer(user_profiles,many=True)
        return Response(serializers.data)

@permission_classes([AllowAny,])
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username=serializer.validated_data['username']
        receiver=serializer.validated_data['email']
        user = serializer.save()
        user.refresh_from_db()
            # user.is_active = False
        user.save()
        sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
        msg = "Nice to have you on board LogOnGo. Let's get to work!</p> <br> <small> The welcome committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
        message = Mail(
            from_email = Email("davinci.monalissa@gmail.com"),
            to_emails = receiver,
            subject = "You're in!",
            html_content='<p>Hello, ' + str(username) + '! <br><br>' + msg
        )
        try:
            sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
            response = sendgrid_client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
        status_code = status.HTTP_201_CREATED
        token = AuthToken.objects.create(user)
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            "token": token[1]
            }
        return Response(serializer.data)

@permission_classes([AllowAny,])
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = MyUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        try:
            token = AuthToken.objects.create(user)[1]
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        response = Response()

        response.set_cookie(key='knox', value=token, httponly=True)
        response.data = {
            'token': token,
            'email':user.email,
            'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'id':user.id,
            'is_staff':user.is_staff,
            'is_superuser':user.is_superuser,
        }
        return response 

@permission_classes([IsAuthenticated,])
class UserView(APIView):
    # renderer_classes = (UserJSONRenderer)
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = MyUser.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

@permission_classes([IsAuthenticated,])
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('knox')
        response.data = {
            'message': 'success'
        }
        return response

class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,IsAdminUser,)
    serializer_class = ChangePasswordSerializer

@permission_classes([AllowAny,])
class PasswordResetRequest(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            receiver = request.data['email']
            username = request.data['username']
            user = MyUser.objects.filter(email=receiver,username=username).first()
            if user is None:
                raise AuthenticationFailed('User not found!')
                
            serializer.save()
            user_id = user.id
            current_site = get_current_site(request)
            myHtml = render_to_string('reset-pass.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user_id)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "<p>We have received your request to reset the password for your account at LogOnGo.</p><p>Please follow the link below to reset your old password and create a new one:</p> <br> <p></p> <br><br> <small> The welcome committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = "Password Reset Request",
                html_content='<p>Hello, ' + str(username) + ', <br><br>' + myHtml
            )
            print(message)
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)

            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                'message': 'Password reset link sent successfully. Please check your email.',
                }
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def activate(request, uidb64, token):
        permission_classes = (AllowAny,)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(pk=uid)
            print("found user with id:", uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            uid = force_str(urlsafe_base64_decode(uidb64))
            print("uid decoded:",uid)
            user = None 
            print("no user")
        if user is not None and account_activation_token.check_token(user, token):
            print("success")
            response = Response()
            successMsg = 'Confirmed! Activation link is valid.'
            response.data = {
                'success':successMsg,
            }
            # return response 
            return redirect('http://localhost:4200/auth/confirmed/password/reset' + uid)
            # return redirect('https://log-on-go.web.app/auth/confirmed/password/reset/' + uid)
        else:
            Http404
            print("failure")
            response = Response()
            errorMsg = 'Sorry, activation link is invalid.'
            response.data = {
                'error':errorMsg,
            }
            return response 
            # serializer = PasswordResetSerializer
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,IsAdminUser)
    serializer_class = PasswordResetSerializer

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UpdateSerializer
        
        



