from rest_framework import status, generics
from rest_framework.response import Response
from ..models import FriendShipRequest, Profile
from ..serializers.friends import FriendShipSerializer, AcceptFriendSerializer, RejectSerializer, CancelSerializer, RemoveFriendSerializer



class FriendsRequestManager(generics.GenericAPIView):

    queryset = FriendShipRequest.objects.all()
    serializer_class = FriendShipSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user = Profile.objects.get(username="Sara2")
        query_params = request.query_params
        if query_params:

            for key in query_params.keys():
                if hasattr(self.get_queryset().choices, key):
                    filter_kwargs = {key: query_params[key]}
                    self.queryset = self.get_queryset().filter(**filter_kwargs)
        return Response(self.get_queryset())
    
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
    def post(self, request, *args, **kwargs):
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
        print("------->>", data)
        user = data['user']
        friend_id = data['friend']
        user.friends.remove(friend_id)
        return Response({"message": "Friend removed"}, status=status.HTTP_200_OK)