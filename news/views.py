from rest_framework import viewsets, generics, status, serializers
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import filters
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import News, Comment, Status, NewsStatus, CommentStatus
from .serializers import NewsSerializer, CommentSerializer, StatusSerializer, NewsStatusSerializer, \
    CommentStatusSerializer
from .permissions import NewsPermission


class PostPagePagination(PageNumberPagination):
    page_size = 3


class NewsViewSet(viewsets.ModelViewSet):
    """
    API для создания, получения, изменения и удаления новостей
    """

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [NewsPermission]
    pagination_class = PostPagePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['updated', 'created', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API для создания, получения, изменения и удаления комментариев
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [NewsPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news_id=self.kwargs.get('news_id')
        )


class StatusViewSet(viewsets.ModelViewSet):
    """
    API для создания, получения, изменения и удаления статусов
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAdminUser]


class StatusNewsViewSet(viewsets.ModelViewSet):
    """
    API для добавления статуса новости
    """
    queryset = NewsStatus.objects.all()
    serializer_class = NewsStatusSerializer

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))


class StatusCommentViewSet(viewsets.ModelViewSet):
    """
    API для добавления статуса комментарию
    """
    queryset = CommentStatus.objects.all()
    serializer_class = CommentStatusSerializer

    def get_queryset(self):
        return super().get_queryset().filter(comment_id=self.kwargs.get('comment_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            comment_id=self.kwargs.get('comment_id')
        )


@api_view(['GET'])
def create_news_status(request, news_id, slug):
    try:
        news_status = NewsStatus.objects.create(
            status=Status.objects.get(slug=slug),
            author=request.user.author,
            news_id=news_id
        )
    except Exception as e:
        return Response({'error': 'Already created'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Status added'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def create_comment_status(request, news_id, comment_id, slug):
    try:
        comment_status = CommentStatus.objects.create(
            status=Comment.objects.get(slug=slug),
            author=request.user.author,
            comment_id=comment_id
            # news_id=news_id
        )
    except Exception as e:
        return Response({'error': 'Already created'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Status added'}, status=status.HTTP_201_CREATED)
