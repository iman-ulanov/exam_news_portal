from rest_framework import viewsets

from .models import Author
from .serializers import AuthorRegisterSerializer


class AuthorRegisterApiView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer
    authentication_classes = []
