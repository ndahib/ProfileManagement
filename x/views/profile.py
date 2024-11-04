from ..models import Profile
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers.profile import ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

# from rest_framework.permissions import  IsAuthenticated


#########################CRUD OPERATIONS#####################################
class Profiles(ListCreateAPIView,
               RetrieveUpdateDestroyAPIView):
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    # add Permission Later 

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        for key, value in query_params.items():
            if hasattr(Profile, key):
                filter_kwargs = {key: value}
                queryset = queryset.filter(**filter_kwargs)
        return queryset


    def get_queryset(self):
        queryset = Profile.objects.all()
        return self.filter_queryset(queryset)
 

    def get_object(self):
        # print("**************>>", Profile)
        return get_object_or_404(Profile, username="ndahib") 
        # to change later with username = self.request.user.username (generalize)


    def perform_destroy(self, instance):
        instance.delete()
        # Make API call to delete the account from the authentication db
        # return Response(status=status.HTTP_204_NO_CONTENT)


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        
        if "avatar" in request.data:
            avatar = request.data["avatar"]
            if avatar is None or avatar == "":
                request.data["avatar"] = settings.DEFAULT_AVATAR
        return super().partial_update(request, *args, **kwargs)



##########################My Profile##########################
class MyProfile(Profiles):
    """
    Retrieve or update the authenticated user's profile.
    """

    def get_queryset(self):
        """Return the authenticated user's profile."""

        self.request.user.username = "ndahib"
        return Profile.objects.filter(username=self.request.user.username)


    def get(self, request, *args, **kwargs):
        """Retrieve the authenticated user's profile."""
        query_params = request.query_params
        instance = self.get_object()

        fields_to_retrieve = {
            key: getattr(instance, key) for key in query_params.keys() if hasattr(instance, key)
        }
        if "friends" in fields_to_retrieve:
            friends_queryset = instance.friends.all()
            friends_serializer = ProfileSerializer(friends_queryset, many=True)
            fields_to_retrieve["friends"] = friends_serializer.data

        if fields_to_retrieve:
            return Response(fields_to_retrieve, status=status.HTTP_200_OK)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
