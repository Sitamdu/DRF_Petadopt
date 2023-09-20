from .models import *
from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import PetSerializer, AdoptSerializer, ProductSerializer,UserSerializerWithToken,UserSerializer
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from pet.permissions import AdminOrReadOnly, RequesterOrReadOnly
from .pagination import PetsListPagination,PetListLOPagination,PetListCPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password


class MyTokenObtainPairSeializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # data['username'] = self.user.username
        # data['email'] = self.user.email

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSeializer

class AdoptFilter(generics.ListAPIView):
    serializer_class = AdoptSerializer


    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return AdoptionRequest.objects.filter(requester__username=username)

    # query parameter
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return AdoptionRequest.objects.filter(requester__username=username)


# using Class

class PetList(APIView):

    def get(self,request):
        pet = Pet.objects.all()
        serializer = PetSerializer(pet, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class PetDetail(APIView):

    def get(self,request,pk):
        try:
            pet = Pet.objects.get(pk=pk)
        except:
            return Response({'error': 'pet not found'},status=status.HTTP_204_NO_CONTENT)

        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def put(self,request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        pet = Pet.objects.get(pk=pk)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(APIView):
    def get(self,request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


class AdoptionList(APIView):
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        query = AdoptionRequest.objects.all()
        serializer = AdoptSerializer(query, many=True)
        return Response(serializer.data)

class AdoptionDetail(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            detail = AdoptionRequest.objects.get(pk=pk)
        except:
            return Response({'error': 'pet not found'}, status=status.HTTP_204_NO_CONTENT)
        serializer = AdoptSerializer(detail)
        return Response(serializer.data)

    def put(self,request):
        serializer = AdoptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# FCB using decorator


@api_view(['POST'])

def register(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name = data['username'],
            username = data['username'],
            email = data['email'],
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exits'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    users = request.user
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
#
# @api_view(['GET','POST'])
# def pet_list(request):
#
#     if request.method == 'GET':
#         pet = Pet.objects.all()
#         serializer = PetSerializer(pet, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = PetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def pet_detail(request,pk):
#
#     if request.method == 'GET':
#
#         try:
#             pet = Pet.objects.get(pk=pk)
#         except:
#             return Response({'error': 'pet not found'},status=status.HTTP_204_NO_CONTENT)
#
#         serializer = PetSerializer(pet)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         serializer = PetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         pet = Pet.objects.get(pk=pk)
#         pet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# using generic
class PetList(generics.ListCreateAPIView):
    pagination_class = PetsListPagination
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    # filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    filter_backends = [filters.OrderingFilter]
    # filterset_fields = ['name', 'age', 'size']
    # search_fields = ['name','color']
    ordering_fields = ['age']



class PetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class AdoptList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptSerializer

class AdoptDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [RequesterOrReadOnly]
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptSerializer
