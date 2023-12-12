from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from api.models import CustomUser,Schedule,Vehicle


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class ScheduleSerializer(serializers.ModelSerializer):
    model=Schedule
    fields=['vehicle_id','datescheduled','start_time','end_time']


    def create(self, validated_data):
        return Schedule.objects.create(**validated_data )
    
class VehicleSerializer(serializers.ModelSerializer):
    model=Vehicle
    fields=[' vehicle_owner','vehicle_no','model']
    
    def create(self, validated_data):
        return Vehicle.objects.create(**validated_data )
    
    
    
    
    
    