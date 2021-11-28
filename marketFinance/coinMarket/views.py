from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

from .models import User
from .serializer import *

import datetime

# Create your views here.
class UserRegisterView(APIView):
    permission_classes = [ permissions.AllowAny]
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'message': 'Register successful!'
                }, status=status.HTTP_201_CREATED)

            else:
                return Response({
                    'error_message': 'This email has already exist!',
                    'errors_code': 400,
                }, status=status.HTTP_400_BAD_REQUEST)        
        except:
            return Response({
                "error_message":"Oops! Something went wrong! Help us improve your experience by sending an error report"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          


class UserLoginView(APIView):
    permission_classes = [ permissions.AllowAny]
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = authenticate(
                    request,
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password']
                )
                if user:
                    refresh = TokenObtainPairSerializer.get_token(user)
                    data = {
                        'refresh_token': str(refresh),
                        'access_token': str(refresh.access_token)
                    }
                    return Response(data, status=status.HTTP_200_OK)
                    
                return Response({
                    'error_message': 'Email or password is incorrect!',
                    'error_code': 400
                }, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({
                'error_messages': serializer.errors,
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "error_message":"Oops! Something went wrong! Help us improve your experience by sending an error report"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          



class UserDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        try:
            userCheck = request.user.id 
            if userCheck != pk:
                return Response({
                    "error_message":"You don't have permission"
                }, status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(pk=pk)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({
                "error_message":"Oops! Something went wrong! Help us improve your experience by sending an error report"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          

    def put(self, request, pk, format=None):
        try:
            userCheck = request.user.id 
            if userCheck != pk:
                return Response({
                    "error_message":"You don't have permission"
                }, status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(pk=pk)
            serializer = UserUpdateSerializer()
            data = serializer.update(user,validated_data=request.data)
            return Response({
                "message": "update successful !"
            }, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({
                "error_message":"Oops! Something went wrong! Help us improve your experience by sending an error report"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          


class CoinInfo(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        try:
            typecoin = TypeCoin.objects.all()
            serializer = CoinInfoSerializer(typecoin, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({
                "error_message":"Oops! Something went wrong! Help us improve your experience by sending an error report"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          

class CoinData(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk, time , format=None):
        try: 
            validTime = {'day': 1 , 'week': 7, 'month': 30}
            if time not in validTime:
                return Response({
                "error_message":"The time in the url invalid"
            }, status=status.HTTP_400_BAD_REQUEST) 
            
            coindata = Coin.objects.filter(typeCoin__id=pk, time__second__lt=3 ,time__lte=datetime.datetime.today(), time__gt=datetime.datetime.today()-datetime.timedelta(days=validTime[time])).order_by('-time')
            print(time)
            serializer = CoinDataSerializer(coindata, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({
                "error_message":"Oops! Something went wrong! Help us improve your experience by sending an error report"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          
