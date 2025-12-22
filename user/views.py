
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
class User_login_page(APIView):
    def post(self,request):
        if "username" not in request.data and "password" not in request.data:
            return Response({"message":"username and password are required"},status=400)
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)
        if user is None:
            return Response(
                {"message": "Invalid username or password"},
                status=401
            )
        refresh = RefreshToken.for_user(user=user)
        update_last_login(None,user) # type: ignore
        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user":{
                "user_id":user.id  # type: ignore
            }
        }, status=200)
    

    
class User_logout_page(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if "refresh" not in request.data:
            return Response({"message":"Refresh token is required for logout"},status=400)
        refresh = request.data.get("refresh")
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return  Response({"message":"Logout is succesfull"},status=200)
        except:
            return  Response({"message":"Logout is unsuccesfull"},status=400)

class Refersh_access_token(APIView):
    def post(self,request):
        if "refresh" not in request.data:
            return Response({"message":"Refresh token is required for logout"},status=400)
        refresh = request.data.get("refresh")
        access = RefreshToken(refresh).access_token
        return Response({"access":str(access)},status= 200)
        
        



        



