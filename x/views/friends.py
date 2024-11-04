from rest_framework import status, generics
from rest_framework.response import Response
from ..models import FriendShipRequest, Profile
from ..serializers.friends import FriendShipSerializer, AcceptFriendSerializer, RejectSerializer, CancelSerializer, RemoveFriendSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class FriendsRequestManager(generics.GenericAPIView):

    serializer_class = FriendShipSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # self.request.user = Profile.objects.get(username="ndahib") # to change later
        self.queryset = FriendShipRequest.objects.filter(
                Q(sender_profile=self.request.user) | Q(receiver_profile=self.request.user)
        )
        return super().get_queryset()

    def get(self, request):
        query_params = request.query_params
        friend_requests = self.get_queryset()

        if query_params:
            status_map = {'pending': 0, 'accepted': 1, 'rejected': 2}
            for request_status in query_params:
                if request_status in status_map:
                    friend_requests = friend_requests.filter(status=status_map[request_status])
        
        serialized_data = self.get_serializer(friend_requests, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Friend request sent"},
                         status=status.HTTP_201_CREATED)
    

class AcceptFriendRequest(generics.CreateAPIView):

    ### no need to let the request in db if accepted return accept to send maybe notification to user of alert without status in db
    queryset = FriendShipRequest.objects.all()
    serializer_class = AcceptFriendSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class RejectFriendRequest(generics.DestroyAPIView):

    queryset = FriendShipRequest.objects.all()
    serializer_class = RejectSerializer
    def destroy(self, request, *args, **kwargs):
        request.user = Profile.objects.get(username="HamzaElmoudden")
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.validated_data
        self.perform_destroy(instance)
        return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)


class CancelFriendRequest(generics.DestroyAPIView):

    queryset = FriendShipRequest.objects.all()
    serializer_class = CancelSerializer
    def post(self, request, *args, **kwargs):
        request.user = Profile.objects.get(username="ndahib")
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.validated_data
        self.perform_destroy(instance)
        return Response({"message": "Friend request canceled"}, status=status.HTTP_200_OK)
    
class RemoveFriend(generics.GenericAPIView):

    queryset = Profile.objects.all()
    serializer_class = RemoveFriendSerializer

    def post(self, request, *args, **kwargs):
        request.user = Profile.objects.get(username="HamzaElmoudden")
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data['user']
        friend_id = data['friend']
        user.friends.remove(friend_id)
        return Response({"message": "Friend removed"}, status=status.HTTP_200_OK)