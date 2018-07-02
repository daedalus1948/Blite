from django.test import TestCase, Client
from django.contrib.auth.models import User


class CommentViewCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="test_user")
        user.set_password("test_password")
        user.save()

    def test_user_creation_valid_form(self):
        user_form = {"username":"test_user1", "password1":"test_password", "password2":"test_password"}
        response = self.client.post('/users/register/', user_form)
        self.assertEqual(response.status_code, 302)

    def test_user_creation_invalid_form(self):
        user_form = {"username":"test_user2", "password1":"test_password", "password2":"wrong_password"}
        response = self.client.post('/users/register/', user_form)
        self.assertEqual(response.status_code, 400)

    def test_user_update_valid_form(self):
        self.client.login(username="test_user", password="test_password")
        user_form = {"HTTP_method":"PUT", "first_name":"test_firstname", "last_name":"test_lastname", "email":"test_email@test.com"}
        response = self.client.post('/users/1/', user_form)
        self.assertEqual(response.status_code, 302)

    def test_user_update_invalid_form(self):
        self.client.login(username="test_user", password="test_password")
        user_form = {"HTTP_method":"PUT", "email":"wrong_email_format"}
        response = self.client.post('/users/1/', user_form)
        self.assertEqual(response.status_code, 400)

    def test_user_delete_valid_form(self):
        self.client.login(username="test_user", password="test_password")
        user_form = {"HTTP_method":"DELETE", "confirmation":"YES"}
        response = self.client.post('/users/1/', user_form)
        self.assertEqual(response.status_code, 302)

    def test_user_delete_invalid_form(self):
        self.client.login(username="test_user", password="test_password")
        user_form = {"HTTP_method":"DELETE", "confirmation":"NO"}
        response = self.client.post('/users/1/', user_form)
        self.assertEqual(response.status_code, 400)

    def test_user_logout_get_request(self):
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 405) # get request not allowed

    def test_user_logout_post_request(self):
        response = self.client.post('/users/logout/')
        self.assertEqual(response.status_code, 302)

    def test_user_login_valid_form(self):
        response = self.client.post('/users/login/', {"username":"test_user", "password":"test_password"})
        self.assertEqual(response.status_code, 302)

    def test_user_login_invalid_form(self):
        response = self.client.post('/users/login/', {"username":"test_user", "password":""})
        self.assertEqual(response.status_code, 400)





