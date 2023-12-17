from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import CustomUser,Wallet,Vehicle,Schedule
from django.core.exceptions import ObjectDoesNotExist
from .user_serializer import CustomUserSerializer,ScheduleSerializer,VehicleSerializer,ticketserializer
from rest_framework.exceptions import APIException
from django.contrib.auth.hashers import make_password, check_password
import datetime
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        EoM = data.get('EmailOrUsername')
        if EoM is None:
            raise APIException('EmailOrUsername is a mandatory field.')
        try:
            user = CustomUser.objects.get(username = EoM)
        except ObjectDoesNotExist:
            user = None
        if user is None:
            try:
                user = CustomUser.objects.get(email = EoM)
            except ObjectDoesNotExist:
                user = None
        
        if user is None:
            raise APIException('Invalid Credentials')

        if not user or not check_password(request.data['password'], user.password):
            raise APIException('Invalid Credentials')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
        response.data = {
            'access-token': access_token,
            'refresh-token': refresh_token
        }

        return response

class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token' : access_token
        })
    

class LogoutAPIView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key = "refreshToken")
        response.data = {
            'message': "SUCCESS"
        }
        return response

        
class updateprofile(APIView):
    
    def get(self, request, format =None):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        
        queryset = CustomUser.objects.filter(id=user_id)
        return Response(CustomUserSerializer(queryset,many=True).data)
        
    
    
    def patch(self,request):
        
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        data=request.data
        task=CustomUser.objects.filter(id=user_id)
        serializer = CustomUserSerializer(task[0],data=data,partial=True)   
        if not serializer.is_valid():
            return Response({
                'data': serializer.errors,   
                'message':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
                            'data': serializer.data,   
                            'message':'updated succesfully'},
                            status=status.HTTP_201_CREATED)  
class addvehicle(APIView):
    
    def get(self,request):
       
            token = request.headers.get('Authorization', '').split(' ')[1]
            user_id = decode_access_token(token)
            tasks=Vehicle.objects.filter( vehicle_owner=user_id)
            serializer= VehicleSerializer(tasks,many=True)
            
            return Response({
                    'data': serializer.data,   
                    'message':'vehicle fetched succesfully'},status=status.HTTP_201_CREATED)       
    
    def post(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        data=request.data
        data['vehicle_owner']=user_id
        serializer = VehicleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Scheduleview(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        data=request.data
        data['user']=user_id
        serializer = ScheduleSerializer(data=request.data)

        if serializer.is_valid():
           
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
                return Response({'message': 'Slot is already occupied.'}, status=status.HTTP_400_BAD_REQUEST)

       
class Ticketview(APIView):
   
    def get(self, request):
        scheduler_id = request.query_params.get('scheduler_id')
        
        if scheduler_id:
            try:
                schedule_instance = Schedule.objects.get(id=scheduler_id)
                serializer = ticketserializer(schedule_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Schedule.DoesNotExist:
                return Response({'message': 'Schedule not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Scheduler ID not provided in query parameters'}, status=status.HTTP_400_BAD_REQUEST)
    
    
        
        # queryset = CustomUser.objects.all().filter(id=user_id)
        # for i in queryset:
        #     print(i.email)
        #     print(i.username)
        #     print(i.password)  
        
    
        
        
      
        
        
    
        
