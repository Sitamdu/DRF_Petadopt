from django.urls import path
from .views import *


urlpatterns = [
    # FCB
    # path('posts', pet_list, name='pet-list'),
    # path('posts/<str:pk>/', pet_detail, name='pet-detail'),
    path('user/', user_list, name='user-list'),
    path('user/profile/', user_profile, name='user-profile'),

    path('user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    #CB
    # path('posts/', PetList.as_view(), name='pet-list-create'),
    # path('posts/<int:pk>/', PetDetail.as_view(), name='pet-update-delete'),
    path('product/', ProductList.as_view(), name='product-list'),
    path('adopt/', AdoptionList.as_view(), name='adopt-request'),
    path('detail/<int:pk>/', AdoptionDetail.as_view(), name ='adopt-detail'),



    #generics
    path('posts/', PetList.as_view(), name = 'pet-list-Create'),
    path('update/<int:pk>/', PetRetrieveUpdateDestroyView.as_view(), name='update-delete'),
    path('adopt1/', AdoptList.as_view(), name='adopt-detail'),
    path('detail1/<int:pk>/', AdoptDetail.as_view(), name='adopt-detail'),

    #filter
    path('adopt/<str:username>/', AdoptFilter.as_view(), name = 'pet-filter'),
    path('adopt/', AdoptFilter.as_view(), name='pet-filter'),

]
