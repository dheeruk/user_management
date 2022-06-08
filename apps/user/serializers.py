from dataclasses import fields
from rest_framework import serializers
from .models import Address, Hobbies, User,UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password']

    def validate(self, request):
        return request

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(self.initial_data.get("password"))
        user.save()
        return user
        

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserHobbiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobbies
        fields = '__all__'




class GetUserDataSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','profile_data']

    def get_profile_data(self,obj):
        try:
            serializer = UserProfileSerializer(UserProfile.objects.get(user__id=obj.id))
            profileData = serializer.data
            if profileData.get('address') and len(profileData.get('address'))>0:
                addressData = []
                for addId in profileData.get('address'):
                    addressData.append(UserAddressSerializer(Address.objects.get(id=addId)).data)
                profileData['address'] = addressData
            if profileData.get('hobbies') and len(profileData.get('hobbies'))>0:
                hobbiesData = []
                for hobId in profileData.get('hobbies'):
                    hobbiesData.append(UserHobbiesSerializer(Hobbies.objects.get(id=hobId)).data)
                profileData['hobbies'] = hobbiesData
            return profileData
        except UserProfile.DoesNotExist:
            pass
        return None
    

    

    