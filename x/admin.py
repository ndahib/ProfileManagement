from django.contrib import admin
from .models import Profile, FriendShipRequest, Match

admin.site.register([Profile, FriendShipRequest, Match])
