from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store the hashed password

    def __str__(self):
        return self.username