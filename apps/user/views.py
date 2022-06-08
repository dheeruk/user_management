
from requests import JSONDecodeError
from rest_framework import generics, status
from django.http import JsonResponse
from .models import Hobbies, User,Address, UserProfile

from apps.custom_auth.get_token import MyTokenObtainPairSerializer
from .serializers import GetUserDataSerializer, UserProfileSerializer, UserSerializer,UserAddressSerializer,UserHobbiesSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging,json

logger = logging.getLogger(__name__)


class UserDelete(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request,pk=None):
        try:
            if pk is not None:
                user = User.objects.get(id=pk)
                serialized_data = UserSerializer(user,many=False).data
                user.delete()
                return JsonResponse(serialized_data,status=status.HTTP_200_OK)
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        except BaseException as err:
            return JsonResponse({
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        
 
class GetAllUsers(generics.ListAPIView):
    permission_classes = (AllowAny,)
    def get(self,request):
        try:
            userId = request.GET.get('userId',None)
            if userId is None:
                users = User.objects.all()
                serialized_data = GetUserDataSerializer(users,many=True).data
                return JsonResponse(serialized_data,status=status.HTTP_200_OK,safe=False)
            user = User.objects.filter(id=userId).first()
            serialized_data = GetUserDataSerializer(user,many=False).data
            return JsonResponse(serialized_data,status=status.HTTP_200_OK)
        except BaseException as err:
            logger.exception("failed to get users : ", exc_info=err)
            return JsonResponse({
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetUser(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    def get(self,request,userId):
        try:
            user = User.objects.get(id=userId)
            serialized_data = GetUserDataSerializer(user,many=False).data
            return JsonResponse(serialized_data,status=status.HTTP_200_OK)
        except BaseException as err:
            logger.exception("failed to get users : ", exc_info=err)
            return JsonResponse({
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateUser(generics.CreateAPIView):

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        try:
            logger.info(json.dumps(request.data))

            # create user
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user_data = MyTokenObtainPairSerializer.get_token(User.objects.get(email=request.data.get('email')))
            return JsonResponse(user_data,status=status.HTTP_201_CREATED)
        except BaseException as err:
            logger.exception("failed creating user : ", exc_info=err)
            return JsonResponse({
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateUser(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def put(self, request, *args, **kwargs):
        try:

            user = User.objects.get(id=request.user.id)
            user.email = request.data.get('email') if request.data.get('email',None) is not None else user.email
            user.first_name = request.data.get('first_name') if request.data.get('first_name',None) is not None else user.first_name
            user.last_name =  request.data.get('last_name') if request.data.get('last_name',None) is not None else user.last_name
            user.status = request.data.get('status') if request.data.get('status',None) is not None else user.status
            user.save()
            serializer = UserSerializer(user, many=False)
            logger.info("user updated successfully")
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        except BaseException as err:
            logger.exception(
                "Error Occured While Uodating User  : ", exc_info=err)
            return JsonResponse({
                'message': 'Something terrible went wrong',
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserAddresCreate(generics.CreateAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request.data['user'] = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)

        except BaseException as err:
            logger.exception("failed creating user : ", exc_info=err)
            return JsonResponse({
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserAddressUpdate(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserAddressSerializer
    def put(self, request,addressId):
        try:

            user = User.objects.get(id=request.user.id)
            address = Address.objects.get(id=addressId,user__id=user.id)
            address.city = request.data.get('city') if request.data.get('city',None) is not None else  address.city
            address.state = request.data.get('state') if request.data.get('state',None) is not None else  address.state
            address.zipcode = request.data.get('zipcode') if request.data.get('zipcode',None) is not None else  address.zipcode
            address.country = request.data.get('country') if request.data.get('country',None) is not None else  address.country
            address.save()

            serialized_data = UserAddressSerializer(address).data
            logger.info(f"address updated successfully: {serialized_data}")
            return JsonResponse(serialized_data,status=status.HTTP_202_ACCEPTED)
        except BaseException as err:
            logger.exception(
                "Error Occured While Updating User Address : ", exc_info=err)
            return JsonResponse({
                'message': 'Something terrible went wrong',
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserCreateProfile(generics.CreateAPIView):
    permission_classes =  (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def post(self,request):
        try:
            request.data['user'] = request.user.id
             # checking is address exist for this user
            address = Address.objects.filter(user__id=request.user.id).first()
            if address:
                # adding default address
                request.data['address'] = address.id
            
            hobbies = Hobbies.objects.filter(user__id=request.user.id).first()
            if hobbies:
                # adding default hobbies
                request.data['hobbies'] = hobbies.id

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            profile_data = serializer.data
            logger.info(f"basic user profile created successfully : {profile_data}")
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)

        except BaseException as err:
            logger.exception(
                "Error Occured While Creating User Profile : ", exc_info=err)
            return JsonResponse({
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserProfileUpdate(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
  
    def put(self, request):
        try:

            user = User.objects.get(id=request.user.id)
            userProfile = UserProfile.objects.get(user__id=user.id)
            userProfile.image = request.data.get('image') if request.data.get('image',None) is not None else userProfile.image
            userProfile.phone = request.data.get('phone') if request.data.get('phone',None) is not None else userProfile.phone

            # updating given address ids in the form of array
            if request.data.get("addressIds",None) is not None and len(json.loads(request.data.get("addressIds")))>0:
                addressIds =  json.loads(request.data.get("addressIds"))
                userProfile.address.clear()
                for addId in addressIds:
                    try:
                        address = Address.objects.get(user__id=user.id,id=addId)
                        userProfile.address.add(address)
                    except Address.DoesNotExist:
                        logger.error(f"error occured while getting address for given address id : {addId}")
             # updating given hobbies ids in the form of array
            if request.data.get('hobbiesIds',None) is not None and len(json.loads(request.data.get("hobbiesIds")))>0:
                hobbiesIds =  json.loads(request.data.get("hobbiesIds"))
                userProfile.hobbies.clear()
                for hobId in hobbiesIds:
                    try:

                        hobbies = Hobbies.objects.get(user__id=user.id,id=hobId)
                        userProfile.hobbies.add(hobbies)
                    except Address.DoesNotExist:
                        logger.error(f"error occured while getting address for given address id : {hobId}")

            userProfile.save()
            serialized_data = UserProfileSerializer(userProfile).data
            logger.info(f"user profile updated successfully: {serialized_data}")
            return JsonResponse(serialized_data,status=status.HTTP_202_ACCEPTED)
        except BaseException as err:
            logger.exception(
                "Error Occured While Updating User Details : ", exc_info=err)
            return JsonResponse({
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class UserHobbiesCreate(generics.CreateAPIView):
    serializer_class = UserHobbiesSerializer
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            request.data['user'] = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return JsonResponse(serializer.data,status=status.HTTP_201_CREATED)

        except BaseException as err:
            logger.exception("failed creating user hobbies : ", exc_info=err)
            return JsonResponse({
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserHobbiesUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserHobbiesSerializer
    def put(self,request,hobbiesId):
        try:

            user = User.objects.get(id=request.user.id)
            hobbies = Address.objects.get(id=hobbiesId,user__id=user.id)
            hobbies.name = request.data.get('name') if request.data.get('name',None) is not None else  hobbies.name
            hobbies.save()
            serialized_data = UserHobbiesSerializer(hobbies).data
            logger.info(f"hobbies updated successfully: {serialized_data}")
            return JsonResponse(serialized_data,status=status.HTTP_202_ACCEPTED)
        except BaseException as err:
            logger.exception(
                "Error Occured While Updating hobbies : ", exc_info=err)
            return JsonResponse({
                'error': str(err)
            },
                safe=False,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




  
