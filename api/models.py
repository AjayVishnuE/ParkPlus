from django.db import models
import uuid

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store the hashed password
    
    def __str__(self):
        return self.username
    
class Report(models.Model):
    
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="report_user")
    ticket_id=models.IntegerField()
    description=models.CharField(max_length=100)
    img= models.ImageField(upload_to=None, height_field=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='parkinglog_created_by')

    def __str__(self):
        return self.id
    
class Wallet(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="wallet_user")
    coin=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallet_created_by')
    
    def __str__(self):
        return self.id


    
    
    
