from django.conf.urls import url
from django.urls import path
from accounts.views import views

urlpatterns = [
    url(r'^register/$', views.UserRegistrationAPIView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
    url(r'^user-profile/$', views.UserProfileAPIView.as_view(), name='user_profile'),
    path('<int:pk>', views.UserModify.as_view(), name='User_Modify'),
    url(r'^user-list/$', views.UserList.as_view(), name='user_list'),
    url(r'^delete/$', views.UserDelete.as_view(), name='user_delete'),
    url(r'^logout/$', views.UserLogout.as_view(), name='user_logout'),
]
