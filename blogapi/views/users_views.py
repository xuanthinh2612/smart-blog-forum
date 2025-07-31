from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..serializers import ArticleSerializer, UserSerializer, ProfileSerializer
from blogapp.models import Article
from users.models import CustomUser, Profile
from ..const import ARTICLE_STATUS__PUBLISED
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.form import *

class UserInfoAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegister(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def post(self, request):
        # Tách dữ liệu user
        user_data = {
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            profile_data = {
                'user': user.id,  # hoặc object
                'full_name': request.data.get('profile.full_name'),
                'birth_day': request.data.get('profile.birth_day'),
                'bio': request.data.get('profile.bio'),
                'avatar': request.FILES.get('profile.avatar'),
            }
            profile_serializer = ProfileSerializer(data=profile_data)

            if profile_serializer.is_valid():
                profile_serializer.save(user=user)

                return Response({'success': 'Register successful'}, status=201)
            else:
                # Trường hợp form không hợp lệ => trả về form có lỗi
                return Response({
                    'profile_errors': profile_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Trường hợp form không hợp lệ => trả về form có lỗi
            return Response({
                'user_errors': user_serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        user_data = {
            'email': request.data.get('email')
        }

        user_serializer = UserSerializer(instance = request.user, data=user_data, partial=True )

        if user_serializer.is_valid():
            user = user_serializer.save()

            # Chỉ thêm field nếu có mặt trong request
            profile_data = {}

            if request.data.get('profile.full_name') != "":
                profile_data['full_name'] = request.data.get('profile.full_name')

            if request.data.get('profile.birth_day') != "":
                profile_data['birth_day'] = request.data.get('profile.birth_day')

            if request.data.get('profile.bio') != "":
                profile_data['bio'] = request.data.get('profile.bio')

            if 'profile.avatar' in request.FILES:
                profile_data['avatar'] = request.FILES.get('profile.avatar')            
                
            profile_serializer = ProfileSerializer(instance=user.profile , data=profile_data)

            if profile_serializer.is_valid():
                profile_serializer.save()

                return Response({'success': 'Register successful'}, status=201)
            else:
                # Trường hợp form không hợp lệ => trả về form có lỗi
                return Response({
                    'profile_errors': profile_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Trường hợp form không hợp lệ => trả về form có lỗi
            return Response({
                'user_errors': user_serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
    