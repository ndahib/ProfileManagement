from django.contrib import admin
from .models import Profile, FriendShipRequest

admin.site.register([Profile, FriendShipRequest])
