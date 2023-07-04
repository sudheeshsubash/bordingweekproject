from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Password
from django.contrib.auth.hashers import make_password
import re


class LoginLogoutSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField()
    class Meta:
        model = User
        fields = ['email','password','confirm_password']
        extra_kwargs = {"confirm_password":{"write_only":True}}
        
        
    def validate(self, attrs):
        super().validate(attrs)
        email = attrs.get('email')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("password is not same")
        user = authenticate(email=email,password=password)
        attrs['user'] = user
        return attrs


 
class PasswordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password 
        fields = ['password']
        
        



class SignInNewUserSerializer(serializers.ModelSerializer):
    
    '''
    
    '''
    password2 = serializers.CharField(max_length=20)
    class Meta:
        model = User
        fields = [
            'password','password2','email','username',
        ]
        extra_kwargs = {"email":{"required":True}}
        
    
    def validate(self, attrs):
        
        username,password =  attrs.get('username'),attrs.get('password')
        email,password2 = attrs.get('email'),attrs.get('password2')

        validationerror = dict() # this variable store all errors and finnaly raise all errors

        # validation start
        if not re.match(r"^[a-zA-Z\s0-9]+$",password):
            validationerror['password']={f"{password}":"Enter a valid password. This value may contain a-z,A-Z,0-9,Whitespace."}

        if not re.match(r"^[a-zA-Z\s0-9]+$",password2):
            validationerror['password2']={f"{password2}":"Enter a valid password. This value may contain a-z,A-Z,0-9,Whitespace."}
        
        if password != password2:
            raise serializers.ValidationError({"password":f'password , password2 is not same'})
        

        if not re.match(r"^[a-zA-Z0-9\s]+$",username):
            validationerror['username']={f"{username}":'Enter a valid username. This value may contain only letters'}

        if not re.match("^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})$",email):
            validationerror['email'] = {f"{email}":'Enter a valid email.'}

        if len(validationerror) != 0:
            raise serializers.ValidationError(validationerror)
        return attrs
   
   
    def save(self, **kwargs):
        User.objects.create(
            username = self.data.get('username'),
            email = self.data.get('email'),
            password = make_password(self.data.get('password'))
        )