from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginLogoutSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['email','password','confirm_password']
        extra_kwargs = {"confirm_password":{"write_only":True}}
        
    
    def validate(self, attrs):
        super().validate(attrs)
        password = attrs.get('password',None)
        confirm_password = attrs.get('confirm_password',None)
        email = attrs.get('email',None)
        print(email,password,confirm_password)
        if password != confirm_password:
            raise serializers.ValidationError("password is not match")
        user = authenticate(email=email,password=password)
        attrs['user'] = user
        return attrs
    