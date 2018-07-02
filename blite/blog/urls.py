from django.conf.urls import url, include
from django.urls import reverse # for nested templates {% urls %} to work
from .views import PostController, create_post, edit_post, delete_post, search_post

urlpatterns = [
    url(r'^posts/create/', create_post, name="create_post"), # html form submitting to REST CRUD
    url(r'^posts/(?P<post_id>[0-9]+)/edit/', edit_post, name="edit_post"), # html form submitting to REST CRUD
    url(r'^posts/(?P<post_id>[0-9]+)/delete/', delete_post, name="delete_post"), # html form submitting to REST CRUD
    url(r'^posts/(?:(?P<post_id>[0-9]+)/)?$', PostController.as_view(), name="post_controller"), # REST CRUD
    url(r'^posts/search/$', search_post, name="search_post"),
]
