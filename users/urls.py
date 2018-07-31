from django.urls import path
from django.contrib.auth.views import logout

from .views import (
    SignUpView,
    PhoneVerificationView,
    HomeView,
)


urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('verify/', PhoneVerificationView.as_view(), name='verify'),
    path('home/', HomeView.as_view(), name='home'),
    #path('login/', LoginView.as_view(), name="login_url"),
    path('logout/', logout, {'next_page': '/'}),

]
