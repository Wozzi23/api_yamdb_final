from django.urls import include, path
from v1_api.urls import urlpatterns as v1_api_urls

app_name = 'api'

urlpatterns = [
    path('v1/', include(v1_api_urls)),
]
