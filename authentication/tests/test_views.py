from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

class TestViews(TestCase):

    def test_show_register_page(self):
        response=self.client.get(reverse('register'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"authentication/register.html")

    def test_show_login_page(self):
        response=self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"authentication/login.html")

    def test_signup_user(self):
        self.user={
            "username":"usernamet",
            'email':'djangote@gmail.com',
            'password':'Password',
            'password2':'Password',


        }

        response=self.client.post(reverse('register'),self.user)
        self.assertEqual(response.status_code,302) #302 is the redirect status code

    def test_signup_user_with_taken_name(self):
        self.user={
            "username":"usernametb",
            'email':'djangote@gmail.comb',
            'password':'Password',
            'password2':'Password',


        }
        self.client.post(reverse('register'),self.user) #first post request
        response=self.client.post(reverse('register'),self.user) # second duplicate
        self.assertEqual(response.status_code,409) #409 status code

        storage = get_messages(response.wsgi_request)
        message_list=[]

        for message in storage:
            message_list.append(message.message)
        self.assertIn("Username/email is taken", message_list)
