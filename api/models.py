from django.db import models
import uuid
import datetime
class CustomUser(models.Model):
    username          = models.CharField(max_length=150, unique=True)
    email             = models.EmailField(unique=True)
    password          = models.CharField(max_length=128) 
    mobile            = models.CharField(max_length=55, default="0123")
    created_at        = models.DateTimeField(auto_now_add=True)
    #created_by

    def __str__(self):
        return self.username
    

class Report(models.Model):
    id                = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user_id           = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="report_user")
    ticket_id         = models.IntegerField()
    description       = models.CharField(max_length=100)
    img               = models.ImageField(upload_to=None, height_field=None,null=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    created_by        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='report_created_by')

    def __str__(self):
        return self.id
    

class Wallet(models.Model):
    id                = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user_id           = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name="wallet_user")
    coin              = models.IntegerField()
    created_at        = models.DateTimeField(auto_now_add=True)
    created_by        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallet_created_by')
    
    def __str__(self):
        return self.id


class Vehicle(models.Model):
    id                = models.UUIDField(primary_key=True, max_length=36, default=uuid.uuid4)
    vehicle_no        = models.CharField(max_length=100)
    vehicle_owner     = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vehicle_user')    
    model             = models.CharField(max_length=255)
    created_at        = models.DateTimeField(auto_now_add=True)
    created_by        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vehicle_created_by')

    def __str__(self):
        return self.vehicle_no


class Location(models.Model):
    id                = models.UUIDField(primary_key=True, max_length=36, default=uuid.uuid4)
    name              = models.CharField(max_length=255)
    loc_link          = models.CharField(max_length=5000)
    # loc_id            = models.CharField()
    amount            = models.CharField(max_length=255)
    features          = models.CharField(max_length=255)
    created_at        = models.DateTimeField(auto_now_add=True)
    created_by        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='location_created_by')


class ParkinLog(models.Model):
    id                = models.UUIDField(primary_key=True, max_length=36, default=uuid.uuid4)
    user              = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='parkingLog_user')
    vehicle           = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='parkingLog_vehicle')
    location          = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='parkingLog_location')
    total_amount      = models.CharField(max_length=50)
    fromaddr          = models.CharField(max_length=5000)
    toaddr            = models.CharField(max_length=5000)
    approve           = models.CharField(max_length=5000)
    features          = models.CharField(max_length=5000)
    created_at        = models.DateTimeField(auto_now_add=True)
    created_by        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='parkinglog_created_by')

    def __str__(self):
        return self.id
    

class Transaction(models.Model):
    id                = models.UUIDField(primary_key=True, max_length=36, default=uuid.uuid4)
    user              = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transaction_user')
    wallet            = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_wallet')
    amount            = models.CharField(max_length=255)
    created_at        = models.DateTimeField(auto_now_add=True)
    created_by        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transaction_created_by')
    

class Schedule(models.Model):
    vehicle_id       =  models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='User_vehicle')
    datescheduled    =  models.DateField()
    start_time       =  models.TimeField()
    end_time         =  models.TimeField()  
    # features         =  models.TextField()
    created_at       =  models.DateTimeField(auto_now_add=True)
    created_by       =  models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schedule_created_by')
    # location       =  
    

    
    
    
    
        
    
