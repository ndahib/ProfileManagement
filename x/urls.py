from django.urls import re_path
from .views.profile import Profiles, MyProfile, Friends

urlpatterns = [
    re_path(r'^me', MyProfile.as_view(), name="profile_detail"),
    re_path(r'^', Profiles.as_view(), name="crud_profile"),
    re_path(r'^profiles/me/friends/<str:username>', Friends.as_view(), name="friends_detail"),
]