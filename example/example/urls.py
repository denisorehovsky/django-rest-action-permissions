from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

apipatterns = [
    path('', include('tweets.urls')),
]

urlpatterns = [
    path('api/v1/', include((apipatterns, 'api'), namespace='api')),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/auth/token/', obtain_auth_token),
    path('admin/', admin.site.urls),
]
