from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Profile

class AddFriendView(APIView):
    # permission_classes = [IsAuthenticated] # or more thant that to see later

    def post(self, request, user_id):
        try:
            friend = Profile.objects.get(id=user_id)
            print("-------->>>>>", request.user.profile)
            # request.user.profile.friends.add(friend.profile)
            return Response({"message": "Friend added successfully!"}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

class RemoveFriendView(APIView):
    # permission_classes = [IsAuthenticated] # or more thant that to see later 

    def delete(self, request, user_id):
        try:
            friend = Profile.objects.get(id=user_id)
            request.user.profile.friends.remove(friend.profile)
            return Response({"message": "Friend removed successfully!"}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



class Friends(AddFriendView, RemoveFriendView):
    pass