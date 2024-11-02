from django.db import models

class Profile(models.Model):
    last_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.CharField(default="vecteezy_kid-play-table-tennis_48115843.png", max_length=255)
    bio = models.TextField(max_length=500, blank=True, null=True)
    level = models.IntegerField(default=0, blank=True, null=True)
    username = models.CharField(unique=True, max_length=100)
    friends = models.ManyToManyField("self", blank=True)
   

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    

    
