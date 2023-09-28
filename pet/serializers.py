from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields =['username','email','name','isAdmin']
    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == "":
            name = obj.email

        return name



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id','username','email','name','isAdmin','token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class PetSerializer(serializers.ModelSerializer):
    #adding custom field
    # len_name = serializers.SerializerMethodField()
    class Meta:
        model = Pet
        fields = '__all__'


    # def get_len_name(self, object):
    #     length = len(object.name)
    #     return length


    def validate(self, data):
        if data['name'] == data['species']:
            raise serializers.ValidationError("Name and species cant be same!")
        else:
            return data

    def validated_name(self, value):
        if len(value) > 2:
            raise serializers.ValidationError("Name is too short!")
        else:
            return value


class AdoptSerializer(serializers.ModelSerializer):
    adoption_requests = PetSerializer(many=True, read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = '__all__'




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



