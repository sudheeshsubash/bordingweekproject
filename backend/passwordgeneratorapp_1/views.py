from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)