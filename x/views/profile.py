from ..models import Profile
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.permissions import  IsAuthenticated
from ..serializers.profile import ProfileSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response


#########################CRUD OPERATIONS########################

class Profiles(ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Profile.objects.all()
        query_params = self.request.query_params
        for key, value in query_params.items():
            filter_kwargs = {key: value}
            queryset = queryset.filter(**filter_kwargs)
        return queryset

    def get_object(self):
        # username = self.request.user.username
        # print("enter here", username)
        # if username:
        return get_object_or_404(Profile, username="ndahib")

        raise Http404("Profile not found")

    def perform_destroy(self, instance):
        instance.delete()
        # Make API call to delete the account from the authentication db
        # return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        if request.data.get("avatar") is None or request.data.get("avatar") == "":
            request.data["avatar"] = ""
        return super().partial_update(request, *args, **kwargs)

##########################My Profile##########################

class MyProfile(Profiles):

    # Add Permissions
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(username=self.request.user.username) # or id to change later 
    
    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        instance = self.get_object()

        if query_params:
            fields_to_retrieve = {}
            for key in query_params.keys():
                if hasattr(instance, key):
                    fields_to_retrieve[key] = getattr(instance, key)
                if key == "friends":
                    fields_to_retrieve["friends"] = instance.friends.all()
            if fields_to_retrieve:
                return Response(fields_to_retrieve)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
