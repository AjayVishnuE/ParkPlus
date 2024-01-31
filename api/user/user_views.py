from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from api.models import CustomUser, Wallet, Vehicle, Schedule, Transaction
from .user_serializer import CustomUserSerializer, ScheduleSerializer, VehicleSerializer, TicketSerializer, WalletSerializer, TransactionSerializer
from rest_framework.exceptions import APIException
from django.contrib.auth.hashers import check_password
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from datetime import datetime

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
            user = CustomUser.objects.get(username=EoM)
        except ObjectDoesNotExist:
            user = None
        if user is None:
            try:
                user = CustomUser.objects.get(email=EoM)
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
            'token': access_token
        })

class LogoutAPIView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {
            'message': "SUCCESS"
        }
        return response

class UpdateProfile(APIView):
    def get(self, request, format=None):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)

        queryset = CustomUser.objects.filter(id=user_id)
        return Response(CustomUserSerializer(queryset, many=True).data)

    def patch(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        data = request.data
        task = CustomUser.objects.filter(id=user_id)
        serializer = CustomUserSerializer(task[0], data=data, partial=True)
        if not serializer.is_valid():
            return Response({
                'data': serializer.errors,
                'message': 'something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'data': serializer.data,
            'message': 'updated successfully'
        }, status=status.HTTP_201_CREATED)

class AddVehicle(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        tasks = Vehicle.objects.filter(vehicle_owner=user_id)
        serializer = VehicleSerializer(tasks, many=True)
        return Response({
            'data': serializer.data,
            'message': 'vehicle fetched successfully'
        }, status=status.HTTP_201_CREATED)

    def post(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        data = request.data
        data['vehicle_owner'] = user_id
        serializer = VehicleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        data = request.data
        data['user'] = user_id
        serializer = ScheduleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            schedule = Schedule.objects.get(id=serializer.data['id'])
            
           
            money = schedule.calculate_money()
            
            
            extra_money = schedule.calculate_extra_money()
            
           
            wallet = Wallet.objects.get(user_id=user_id)
            total_money = money + extra_money
            if wallet.debit_money(total_money):
                
                schedule.save()
                
               
                transaction = Transaction(user_id=user_id, amount=-total_money, transaction_type='debit')
                transaction.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Insufficient funds in the wallet.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Slot is already occupied.'}, status=status.HTTP_400_BAD_REQUEST)

class TicketView(APIView):
    def get(self, request):
        scheduler_id = request.query_params.get('scheduler_id')

        if scheduler_id:
            try:
                schedule_instance = Schedule.objects.get(id=scheduler_id)
                serializer = TicketSerializer(schedule_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Schedule.DoesNotExist:
                return Response({'message': 'Schedule not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Scheduler ID not provided in query parameters'}, status=status.HTTP_400_BAD_REQUEST)

class WalletView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        wallet = Wallet.objects.get(user_id=user_id)
        transactions = Transaction.objects.filter(user_id=user_id, transaction_type='debit').order_by('-created_at')
        wallet_serializer = WalletSerializer(wallet)
        transactions_serializer = TransactionSerializer(transactions, many=True)
        
        return Response({
            'wallet': wallet_serializer.data,
            'debit_transactions': transactions_serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]
        user_id = decode_access_token(token)
        wallet = Wallet.objects.get(user_id=user_id)
        amount = request.data.get('amount', 0)
        wallet.add_money(amount)
        transaction = Transaction(user_id=user_id, amount=amount, transaction_type='credit')
        transaction.save()
        return Response({'message': 'Money added to wallet successfully'}, status=status.HTTP_200_OK)   