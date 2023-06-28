from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginLogoutSerializer
from rest_framework import permissions
from django.contrib.auth import authenticate,login,logout



class LoginLogout(APIView):
    '''
    credentials : email, password, comfirm_password
    status : 200 success | 400 badrequest
    response : {
        status,
        message,
        data,
    }
    discription : This api for user login and logout
    '''
    # permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        
        serializer = LoginLogoutSerializer(request.data)
        serializer_attr_value = serializer.validate(serializer.data)
        login(request,serializer_attr_value['user'])
        del serializer_attr_value['user']
        return Response({
            'user':f"{serializer_attr_value['email']}",
            "message":'User Logind successfully',
        },status=status.HTTP_200_OK,)