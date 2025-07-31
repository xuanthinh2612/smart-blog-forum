from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..serializers import ArticleSerializer, UserSerializer
from blogapp.models import Article
from users.models import CustomUser
from ..const import ARTICLE_STATUS__PUBLISED
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Public content for Non-Login User
class ArticleDetailAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            article = Article.objects.get(slug=slug, status=ARTICLE_STATUS__PUBLISED)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        except:
            return Response({'error': 'Article Not Found!'})

class ArticleListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        articles = Article.objects.filter(status=ARTICLE_STATUS__PUBLISED).all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

# Private content for Login user    
class ArticlePrivateDetailAPIView(APIView):

    def get(self, request, slug):
        try:
            article = Article.objects.get(slug=slug, author=request.user)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        except:
            return Response({'error': 'Article Not Found!'})

class ArticleMyListAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        articles = Article.objects.filter(author=request.user).all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
