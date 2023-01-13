from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from accounts import views as acc_views
from news import views as ne_views

acc_router = routers.DefaultRouter()
acc_router.register('register', acc_views.AuthorRegisterApiView)
news_router = routers.DefaultRouter()
news_router.register('statuses', ne_views.StatusViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Twitter Clone API",
        default_version='v-0.01-alpha',
        description="API для взаимодействия с Твиттер API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ulanoviman3@gmail.com"),
        license=openapi.License(name="No Licence"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),

    path('api/account/', include(acc_router.urls)),
    path('api/account/token', obtain_auth_token),

    path('api/', include(news_router.urls)),
    path('api/news/', ne_views.NewsViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/news/<int:pk>/', ne_views.NewsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),

    path('api/news/<int:news_id>/comments/', ne_views.CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/news/<int:news_id>/comments/<int:pk>/', ne_views.CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('api/news/<int:news_id>/<str:slug>/', ne_views.create_news_status),
    path('api/news/<int:news_id>/comments/<int:comment_id>/<str:slug>/', ne_views.create_comment_status),

    # documentation URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),

]
