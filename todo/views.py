from django.shortcuts import render
from .forms import TodoForm
from django.views.decorators.csrf import csrf_exempt
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    todos=Todo.objects.all()
    context = {'todos':todos}
    return render(request,'todo/index.html',context)

def create_todo(request):
    form = TodoForm()
    context = {'form':form}

    if request.method == 'POST':
        title = request.POST.get("Title")
        description = request.POST.get("Description")
        is_complete = request.POST.get("is_completed", False)
        print(is_complete)

        todo = Todo()
        todo.title = title
        todo.description = description
        todo.is_completed = True if is_complete == 'on' else False
        todo.save()

        return HttpResponseRedirect(reverse("todo_detail",kwargs={'id':todo.pk}))



    return render(request,'todo/create_todo.html', context)

def todo_detail(request,id):
    return render(request,'todo/todo_detail.html',{})