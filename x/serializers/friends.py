from rest_framework import serializers
from ..models import FriendShipRequest, Profile


class FriendShipSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField(write_only=True, required=True)
    sender_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = FriendShipRequest
        fields = ['receiver_id', 'sender_id']

    def validate(self, data):
        sender_id = 1 # to change later by the authUser
        receiver_id = data['receiver_id']
        sender_profile = Profile.objects.filter(id=sender_id).first()
        receiver_profile = Profile.objects.filter(id=receiver_id).first()

        if not sender_profile or not receiver_profile:
            raise serializers.ValidationError("One or both users do not exist")
    
        if sender_id == receiver_id:
            raise serializers.ValidationError("You can't add yourself as a friend")
        
        elif receiver_profile.friends.filter(id=sender_id).exists():
            raise serializers.ValidationError("You are already friends with this user")
        
        elif self.Meta.model.objects.filter(sender_profile=sender_profile).exists():
            raise serializers.ValidationError("You already sent a friend request to this user")
        
        elif self.Meta.model.objects.filter(receiver_profile=receiver_profile).exists():
            raise serializers.ValidationError("This user already sent a friend request to you")

        return {'sender_profile': sender_profile, 'receiver_profile': receiver_profile}

    def create(self, validated_data):
        return self.Meta.model.objects.create(
            sender_profile=validated_data['sender_profile'],
            receiver_profile=validated_data['receiver_profile']
        )




class AcceptFriendSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField(read_only=True)
    sender_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = FriendShipRequest
        fields = ['receiver_id', 'sender_id']

    def validate(self, data):
        sender_id = data['sender_id'] # to change later by the authUser
        receiver_id = self.context['request'].user.id # to change later with AuthUser
        sender_profile = Profile.objects.filter(id=sender_id).first()
        receiver_profile = Profile.objects.filter(id=receiver_id).first()
        friend_request = self.Meta.model.objects.filter(sender_profile=sender_profile, 
                                                        receiver_profile=receiver_profile).first()

        if not friend_request:
            raise serializers.ValidationError("No friend request found")
        
        if not sender_profile or not receiver_profile:
            raise serializers.ValidationError("One or both users do not exist")
            
        if sender_id == receiver_id:
            raise serializers.ValidationError("You can't accept yourself as a friend")
         
        elif sender_profile.friends.filter(id=receiver_id).exists():
            raise serializers.ValidationError("You are already friends with this user")
        
        return {'sender_profile': sender_profile, 'receiver_profile': receiver_profile, 'friend_request': friend_request}
    
    def create(self, validated_data):
        request = validated_data['friend_request']
        request.status = 1
        request.save()
        validated_data['sender_profile'].friends.add(validated_data["receiver_profile"])
        return (request)
    
class RejectSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField(read_only=True)
    sender_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = FriendShipRequest
        fields = ['receiver_id', 'sender_id']

    def validate(self, data):
        sender_id = data['sender_id'] # to change later by the authUser
        receiver_id = self.context['request'].user.id # to change later with AuthUser
        print("-------------->>", receiver_id)
        sender_profile = Profile.objects.filter(id=sender_id).first()
        receiver_profile = Profile.objects.filter(id=receiver_id).first()
        friend_request = self.Meta.model.objects.filter(sender_profile=sender_profile, 
                                                        receiver_profile=receiver_profile).first()

        if not friend_request:
            raise serializers.ValidationError("No friend request found")
        
        if not sender_profile or not receiver_profile:
            raise serializers.ValidationError("One or both users do not exist")
            
        if sender_id == receiver_id:
            raise serializers.ValidationError("You can't reject yourself as a friend")
         
        return friend_request
    

class CancelSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField(read_only=True)
    reiceiver_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = FriendShipRequest
        fields = ['receiver_id', 'sender_id']

    def validate(self, data):
        receiver_id = data['sender_id'] # to change later by the authUser
        sender_id = self.context['request'].user.id # to change later with AuthUser
        print("-------------->>", sender_id)
        receiver_profile = Profile.objects.filter(id=receiver_id).first()
        sender_profile = Profile.objects.filter(id=sender_id).first()
        friend_request = self.Meta.model.objects.filter(receiver_profile=receiver_profile,
                                                        sender_profile=sender_profile).first()

        if not friend_request:
            raise serializers.ValidationError("No friend request found")
        
        if not sender_profile or not receiver_profile:
            raise serializers.ValidationError("One or both users do not exist")
            
        if sender_id == receiver_id:
            raise serializers.ValidationError("You can't reject yourself as a friend")
         
        return friend_request
    

class RemoveFriendSerializer(serializers.Serializer):
    friend_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Profile.friends
        fields = ['friend_id']
    
    def validate(self, attrs):
        friend_id = attrs['friend_id']
        user = self.context['request'].user
        user_profile = Profile.objects.filter(id=user.id).first()
        if user_profile is None:
            raise serializers.ValidationError("User not found")
        if friend_id == user.id:
            raise serializers.ValidationError("You can't remove yourself as a friend")
        if friend_id not in Profile.objects.values_list('id', flat=True):
            raise serializers.ValidationError("Friend not found")
        return {'user': user_profile, 'friend': friend_id}
