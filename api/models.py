from django.db import models
import uuid
import datetime
class CustomUser(models.Model):
    # id                = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    username          = models.CharField(max_length=150, unique=True)
    email             = models.EmailField(unique=True)
    password          = models.CharField(max_length=128) 
    mobile            = models.CharField(max_length=55, default="0123")
    created_at        = models.DateTimeField(auto_now_add=True)
   

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
    user_id           = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="wallet_user")
    coin              = models.IntegerField()
    created_at        = models.DateTimeField(auto_now_add=True)
    created_by        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallet_created_by')
    
    def __str__(self):
        return self.id
class Transaction(models.Model):
    id                = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user_id           = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="_user")
    amount            = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, blank=True, editable=False)
    created_at        = models.DateTimeField(auto_now_add=True)
    created_by        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='_created_by')
    
    
    def save(self, *args, **kwargs):
       
        self.transaction_type = 'debit' if self.amount < 0 else 'credit'
        super().save(*args, **kwargs)
        
        

class Vehicle(models.Model):
    id                = models.UUIDField(primary_key=True, max_length=36, default=uuid.uuid4)
    vehicle_no        = models.CharField(max_length=100)
    vehicle_owner     = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vehicle_user')    
    model             = models.CharField(max_length=255)
    created_at        = models.DateTimeField(auto_now_add=True)
    # created_by        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vehicle_created_by')
    

    def __str__(self):
        return self.vehicle_no


    

class Schedule(models.Model):
    id                = models.UUIDField(primary_key=True, max_length=36, default=uuid.uuid4)
    user              = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='scheduler_user')
    vehicle_id       =  models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='User_vehicle')
    datescheduled    =  models.DateField()
    start_time       =  models.TimeField()
    end_time         =  models.TimeField() 
    extratime         = models.TimeField(null=True, blank=True) 
    created_at       =  models.DateTimeField(auto_now_add=True)
    # created_by       =  models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schedule_created_by')
    isverfied =         models.BooleanField(default=False)
    location        =   models.CharField(max_length=255)

    
    
    

    def __str__(self):
        return self.location

    
