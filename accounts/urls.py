from django.urls import path
from django.conf.urls.static import static
from django_movie_api import settings
from . views import home_view, LoginView, RegisterUser
import django.contrib.auth.views as AuthViews


urlpatterns = [
    path('', home_view, name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', AuthViews.LogoutView.as_view(), name='logout'),
    path('register', RegisterUser.as_view(), name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)