from django.test import TestCase, Client
from comments.models import Comment
from blog.models import Post
from django.contrib.auth.models import User


class CommentViewCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="test_user")
        user.set_password("test_password")
        user.save()
        public_post = Post.objects.create(title='test_title', content='test_content', published=1, author=user)
        private_post = Post.objects.create(title='test_title', content='test_content', published=0, author=user)
        public_post.save() # id 1
        private_post.save() # id 2
        comment = Comment.objects.create(title='test_comment', content='test_content', author=user, post=public_post)
        comment.save()

    def test_create_comment_authenticated_valid_form_private_post(self): # should 
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/comments/comments/2/', {"title": "test_title", "content": "test_content"})
        self.assertEqual(response.status_code, 400)

    def test_create_comment_authenticated_valid_form_public_post(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/comments/comments/1/', {"title": "test_title", "content": "test_content"})
        self.assertEqual(response.status_code, 302)

    def test_create_comment_authenticated_invalid_form_public_post(self): # missing content
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/comments/comments/1/', {"title": "asdad", "content": ""})
        self.assertEqual(response.status_code, 400)

    def test_edit_comment_authenticated_valid_form_public_post(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/comments/comments/1/', { "HTTP_method": "PUT", "title": "test_title_updated", "content": "test_content_updated"})
        self.assertEqual(response.status_code, 302)

    def test_edit_comment_authenticated_invalid_form_public_post(self): # missing title
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/comments/comments/1/', { "HTTP_method": "PUT", "title": "", "content": "test_content_updated"})
        self.assertEqual(response.status_code, 400)

    def test_delete_comment_authenticated_valid_form_public_post(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/comments/comments/1/', { "HTTP_method": "DELETE", "confirmation": "YES" })
        self.assertEqual(response.status_code, 302)

    def test_delete_comment_authenticated_invalid_form_public_post(self): # confirmation is NO
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/comments/comments/1/', { "HTTP_method": "DELETE", "confirmation": "NO" })
        self.assertEqual(response.status_code, 400)

