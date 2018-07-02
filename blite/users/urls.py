from django.conf.urls import url, include
from .views import UserController, register, login_handler, logout_handler, profile, user_posts, edit_user, delete_user

urlpatterns = [
    url(r'^register/$', register, name="register"),
    url(r'^login/$', login_handler, name="login"),
    url(r'^logout/$', logout_handler, name="logout"),
    url(r'^(?P<user_id>[0-9]+)/edit/$', edit_user, name="edit_user"),
    url(r'^(?P<user_id>[0-9]+)/delete/$', delete_user, name="delete_user"),
    url(r'^(?P<user_id>[0-9]+)/profile/$', profile, name="profile"),
    url(r'^(?P<user_id>[0-9]+)/profile/posts/(?:(?P<filter>[a-z]+)/)?$', user_posts, name="user_posts"),
    url(r'^(?:(?P<user_id>[0-9]+)/)?$', UserController.as_view(), name="user_controller")
    
]