from enum import Enum 
from django.db import models
from django.conf import settings

class Profile(models.Model):
    last_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    avatar = models.CharField(default=settings.DEFAULT_AVATAR, max_length=255)
    bio = models.TextField(max_length=500, blank=True)
    level = models.IntegerField(default=0, blank=True)
    username = models.CharField(unique=True, max_length=100)
    friends = models.ManyToManyField("self", blank=True)
   

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    


class FriendShipRequest(models.Model):

    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Accepted'),
        (2, 'Declined'),
    ]

    sender_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    # to see later what about time if we add them or not 

    def get_status_display(self):
        return self.STATUS_CHOICES[self.status][1]

    def __str__(self):
        return f"{self.sender_profile} -> {self.receiver_profile} : {self.get_status_display()}"
