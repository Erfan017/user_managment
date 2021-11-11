from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.UserRegistrationAPIView.as_view(), name='register'),
    url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
    url(r'^user-profile/$', views.UserProfileAPIView.as_view(), name='user_profile'),
    url(r'^user-list/$', views.UserList.as_view(), name='user_list'),
    url(r'^delete/$', views.UserDelete.as_view(), name='user_delete'),
    url(r'^logout/$', views.UserLogout.as_view(), name='user_logout'),
    # url(r'^password_reset/$', views.PasswordResetAPIView.as_view(), name='password_change'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
