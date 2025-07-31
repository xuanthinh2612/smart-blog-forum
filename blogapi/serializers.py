from rest_framework import serializers
from blogapp.models import Article, Comment
from users.models import CustomUser, Profile


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    # Bỏ valid trường user của profile 
    # Cách 1.1
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        # Cách 1.2
        fields = '__all__'
        # Cách 2
        # exclude = ['user']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'
        # fields = ['id', 'title', 'content', 'author', 'created_at', 'slug', 'profile']
        # read_only_fields = ['id', 'author', 'slug', 'created_at']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
            # Tách dữ liệu nested profile nếu có
            profile_data = validated_data.pop('profile', {})
            password = validated_data.pop('password', None)
            profile = instance.profile

            # Cập nhật user fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            if password:
                instance.set_password(password)

            instance.save()

            # Cập nhật profile fields
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

            return instance

    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        # fields = '__all__'
        fields = ['id', 'title', 'content', 'author', 'created_at', 'slug', 'image', 'status', 'comments']
        read_only_fields = ['id', 'author', 'slug', 'created_at']
