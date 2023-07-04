from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginLogoutSerializer,PasswordListSerializer,SignInNewUserSerializer
from django.contrib.auth import login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
import random
from rest_framework.permissions import IsAuthenticated
from .models import Password
from rest_framework import status, generics



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginLogout(APIView):
    '''
    
    '''
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            # blacklist_token = RefreshToken(token=token)
            # blacklist_token.blacklist()
            logout(request)
            return Response({
                "message":'Logout successfully'
            },status=status.HTTP_200_OK)
        else:
            serializer = LoginLogoutSerializer(request.data)
            serializer_attr_value = serializer.validate(serializer.data)
            if serializer_attr_value.get('user',None):
                login(request, serializer_attr_value.get('user'))
                token = get_tokens_for_user(serializer_attr_value.get('user'))
            return Response({
                'token':token,
                'message':'Login successfully',
            },status=status.HTTP_200_OK)
        
        
class PasswordGenerator(APIView):
    '''
    
    '''
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        password = str()
        for x in range(20):
            ch = chr(random.randint(65,91))
            password+=ch
        request.session['password'] = password
        return Response({
            'password':password
        },status=status.HTTP_201_CREATED)
    
    def post(self, request, *args, **kwargs):
        try:
            password_obj = Password.objects.create(password=request.session['password'])
            password_obj.save()
            request.session.flush()
            return Response({
                'message':'generated password successfully save to database'
            },status=status.HTTP_200_OK)
        except:
            return Response({
                'message':'generate password then save to database'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PasswordList(generics.ListAPIView):
    '''
    
    '''
    queryset = Password.objects.all()
    serializer_class = PasswordListSerializer
    permission_classes = [IsAuthenticated]
    
    
    
class SignInNewUser(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = SignInNewUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message':'Sign In Successfully Completed',
            'email':serializer.data.get('email')
        },status=status.HTTP_200_OK)