from django.shortcuts import render
from .forms import TodoForm

def index(request):
    return render(request,'todo/index.html')

def create_todo(request):
    form = TodoForm()
    context = {'form':form}
    return render(request,'todo/create_todo.html', context)

