from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from api.models import CustomUser,Schedule,Vehicle
import datetime

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


    
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        
        model=Vehicle
        fields=[' vehicle_owner','vehicle_no','model']
    
    def create(self, validated_data):
        return Vehicle.objects.create(**validated_data )
    
    
    
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['vehicle_id', 'datescheduled', 'start_time', 'end_time', 'location']

    

    def validate(self, data):
        
        existing_schedules = Schedule.objects.filter(
            datescheduled=data['datescheduled'], 
            location=data['location'],
            isverfied=True
        )

        start_time = data['start_time']
        end_time = data['end_time']

        for schedule in existing_schedules:
            if self.is_time_overlap(start_time, end_time, schedule.start_time, schedule.end_time):
                raise serializers.ValidationError("Slot is not available. Overlapping schedule.")

        return data
    def is_time_overlap(self, start_time1, end_time1, start_time2, end_time2):
        
        start_time1 = datetime.strptime(start_time1, '%H:%M:%S').time()
        end_time1 = datetime.strptime(end_time1, '%H:%M:%S').time()
        start_time2 = datetime.strptime(start_time2, '%H:%M:%S').time()
        end_time2 = datetime.strptime(end_time2, '%H:%M:%S').time()

       
        overlap = not (end_time1 <= start_time2 or start_time1 >= end_time2)
        return overlap
    
    
    def create(self, validated_data):
        
        validated_data['isverfied'] = True
        return Schedule.objects.create(**validated_data) 
    
    
    
class ticketserializer(serializers.ModelSerializer):
    calculate_total_duration=serializers.SerializerMethodField()
    
    class Meta:
        model = Schedule
        fields = ['vehicle_id', 'datescheduled', 'start_time', 'end_time','calculate_total_duration'] 
    
    
    
    