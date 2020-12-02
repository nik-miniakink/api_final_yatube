from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError

from .models import Post, Comment, Follow, User, Group
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
from .permissons import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_post(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post

    def get_queryset(self):
        queryset = Comment.objects.filter(post=self.get_post()).all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class GroupList(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class FollowList(generics.ListCreateAPIView):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=following__username', '=user__username']

    def perform_create(self, serializer):

        username = self.request.data.get('following')
        following = get_object_or_404(User, username=username)
        user = self.request.user
        follow = Follow.objects.filter(user=user, following=following)
        if follow:
            raise ValidationError()
        serializer.save(user=user, following=following)
