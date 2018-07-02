from django.test import TestCase, Client
from blog.models import Post
from django.contrib.auth.models import User


# methods should start with 'test*' in order for the framework to run them
class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="test_user", password="test_password")
        Post.objects.create(title='test_title', content='test_content', published=1, author=user)

    def test_content_label(self):
        post=Post.objects.get(id=1)
        field_label = Post._meta.get_field('content').verbose_name
        self.assertEquals(field_label,'content')

    def test_title_max_length(self):
        post=Post.objects.get(id=1)
        max_length = Post._meta.get_field('title').max_length
        self.assertEquals(max_length,80)


# you have to specify FULL url for the tests even with both backslashes!
# '/blog/posts/for_test/'
class PostViewCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="test_user") # user_id_1
        user.set_password("test_password") # set_passwords avoids the hashing of the password for test cases
        user.save()
        post = Post.objects.create(title='test_title', content='test_content', published=1, author=user) # post_id_1
        post.save()

    def test_get_posts(self):
        response = self.client.get('/blog/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/posts.html')
        self.assertTrue('items' in response.context)

    def test_get_create_post_form_redirects_anonymous(self):
        response = self.client.get('/blog/posts/create/')
        self.assertRedirects(response, '/users/login/?next=/blog/posts/create/')

    def test_get_create_post_form_authenticated_proceeds(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get('/blog/posts/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_post_anonymous(self):
        response = self.client.post('/blog/posts/', {"title": "test_title", "content": "test_content", "published":"1"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/posts/')

    def test_create_post_authenticated_valid_form(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/blog/posts/', {"title": "test_title", "content": "test_content", "published":"1"})
        self.assertRedirects(response, '/blog/posts/')

    def test_create_post_authenticated_invalid_form(self): # missing content
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/blog/posts/1/', {"title": "asdad", "content": "", "published":"1"})
        self.assertEqual(response.status_code, 400)
    
    def test_edit_post_anonymous(self):
        response = self.client.post('/blog/posts/1/', {"HTTP_method": "PUT", "title": "test_title", "content": "test_content", "published":"1"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/posts/1/')

    def test_edit_post_authenticated_valid_form(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/blog/posts/1/', { "HTTP_method": "PUT", "title": "test_title_updated", "content": "test_content_updated", "published":"1"})
        self.assertRedirects(response, '/blog/posts/')

    def test_edit_post_authenticated_invalid_form(self): # missing title
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/blog/posts/1/', {"HTTP_method": "PUT", "title": "", "content": "test_content", "published":"1"})
        self.assertEqual(response.status_code, 400)

    def test_delete_post_anonymous(self):
        response = self.client.post('/blog/posts/1/', { "HTTP_method": "DELETE", "confirmation": "YES" })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/posts/1/')

    def test_delete_post_authenticated_valid_form(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/blog/posts/1/', { "HTTP_method": "DELETE", "confirmation": "YES" })
        self.assertRedirects(response, '/blog/posts/')

    def test_delete_post_authenticated_invalid_form(self): # confirmation is NO
        self.client.login(username="test_user", password="test_password")
        response = self.client.post('/blog/posts/1/', { "HTTP_method": "DELETE", "confirmation": "NO" })
        self.assertEqual(response.status_code, 400)




