
from django.test import TestCase
from django.urls import reverse
from todo.models import Todo
from django.contrib.messages import get_messages

class TestView(TestCase):

    def test_create_todo(self):
        self.owneR={
            "username":"usernam66",
            'email':'djangote@gmail6.com',
            'password':'Password8',
            'password2':'Password8',
            }
        self.client.post(reverse('register'),self.owneR)
    #     # login
        self.client.post(reverse('login'),self.owneR)
        

        response = self.client.post(reverse('create_todo'),{
            'Title':'Test Title yes',
            'Description':'some desc goes here',
            'owner':self.owneR,
            "is_completed": False,
        })

        all_todos = Todo.objects.all().count()

        self.assertEqual(response.status_code,302)
        self.assertEqual(all_todos,1)
