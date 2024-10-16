from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from resultsUI.views import uploadView
from .libcode import TokenObtainPairView,TokenRefreshView



urlpatterns = [
    path('api/access_token',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',views.Welcome),
    path('api/ec2s1',uploadView.as_view()),
]