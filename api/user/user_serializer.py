from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from api.models import CustomUser, Schedule, Vehicle, Wallet, Transaction
from datetime import datetime


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
        model = Vehicle
        fields = ['id', 'vehicle_owner', 'vehicle_no', 'model']

    def create(self, validated_data):
        
        return Vehicle.objects.create(**validated_data)


class ScheduleSerializer(serializers.ModelSerializer):
    money = serializers.SerializerMethodField()
    extra_money = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'user', 'vehicle_id', 'datescheduled', 'start_time', 'end_time', 'location', 'money', 'extra_money']

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
        # Check if two time intervals overlap
        h1, m1, s1 = start_time1.hour, start_time1.minute, start_time1.second       
        h2, m2, s2 = end_time1.hour, end_time1.minute, end_time1.second       
        h3, m3, s3 = start_time2.hour, start_time2.minute, start_time2.second   
        h4, m4, s4 = end_time2.hour, end_time2.minute, end_time2.second

        total_seconds1 = h1 * 3600 + m1 * 60 + s1      
        total_seconds2 = h2 * 3600 + m2 * 60 + s2       
        total_seconds3 = h3 * 3600 + m3 * 60 + s3     
        total_seconds4 = h4 * 3600 + m4 * 60 + s4

        overlap = not (total_seconds2 <= total_seconds3 or total_seconds1 >= total_seconds4)
        return overlap

    def create(self, validated_data):
       
        validated_data['isverfied'] = True
        return Schedule.objects.create(**validated_data)

    def get_money(self, schedule):
       
        return schedule.calculate_money()

    def get_extra_money(self, schedule):
       
        return schedule.calculate_extra_money()


class TicketSerializer(serializers.ModelSerializer):
    duration_minutes = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['user', 'vehicle_id', 'datescheduled', 'start_time', 'end_time', 'location', 'duration_minutes', 'vehicle']

    def get_vehicle(self, schedule):
        
        if schedule.vehicle_id:
            return schedule.vehicle_id.model, schedule.vehicle_id.vehicle_no
        return None

    def get_duration_minutes(self, schedule):
        # Calculate and return the duration of the schedule in minutes
        start_time = datetime.combine(datetime.today(), schedule.start_time)
        end_time = datetime.combine(datetime.today(), schedule.end_time)

        if start_time and end_time:
            duration = end_time - start_time
            duration_minutes = int(duration.total_seconds() / 60)
            return duration_minutes

        return 0


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user_id', 'coin']

    def update(self, instance, validated_data):
        
        instance.coin = validated_data.get('coin', instance.coin)
        instance.save()
        return instance


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user_id', 'amount', 'transaction_type', 'created_at']

    def to_representation(self, instance):
       
        representation = super().to_representation(instance)
        representation['is_credit'] = instance.amount > 0
        return representation
