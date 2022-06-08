
from django.contrib import admin
from django.urls import path
from .views import CreateUser,UpdateUser,UserAddresCreate,UserAddressUpdate,UserCreateProfile,UserProfileUpdate,UserHobbiesCreate,GetUser,GetAllUsers,UserDelete
urlpatterns = [
    path('create',CreateUser.as_view(),name='create_user'),
    path('update',UpdateUser.as_view(),name='update_user'),
    path('address/create',UserAddresCreate.as_view()),
    path('address/update/<addressId>',UserAddressUpdate.as_view()),
    path('profile/create',UserCreateProfile.as_view()),
    path('profile/update',UserProfileUpdate.as_view()),
    path('hobbies/create',UserHobbiesCreate.as_view()),
    path('<userId>',GetUser.as_view()),
    path('',GetAllUsers.as_view()),
    path('delete/<pk>',UserDelete.as_view()),
]
