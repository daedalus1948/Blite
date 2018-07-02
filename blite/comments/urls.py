from django.conf.urls import url, include
from django.urls import reverse # for nested templates {% urls %} to work
from .views import CommentController, create_comment, edit_comment, delete_comment

urlpatterns = [
    url(r'^comments/new/(?P<post_id>[0-9]+)/$', create_comment, name="create_comment"),
    url(r'^comments/(?P<comment_id>[0-9]+)/edit/', edit_comment, name="edit_comment"),
    url(r'^comments/(?P<comment_id>[0-9]+)/delete/', delete_comment, name="delete_comment"), 
    url(r'^comments/(?:(?P<comment_id>[0-9]+)/)?$', CommentController.as_view(), name="comment_controller")
]
