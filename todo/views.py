from django.shortcuts import render
from .forms import TodoForm
from django.views.decorators.csrf import csrf_exempt
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages 
from django.contrib.auth.decorators import login_required


def get_show_todos(request,todos):

    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter')=='complete':
            return todos.filter(is_completed=True)
        elif request.GET.get('filter')=='incomplete':
            return todos.filter(is_completed=False)

    return todos

@login_required
def index(request):
    todos=Todo.objects.filter(owner=request.user)
    completed_count = todos.filter(is_completed=True).count()
    incompleted_count = todos.filter(is_completed=False).count()
    all_count = todos.count()
    context = {'todos':get_show_todos(request,todos),
    'all_count':all_count,'completed_count':completed_count,'incompleted_count':incompleted_count,
    }

    return render(request,'todo/index.html',context)

@login_required
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
        todo.owner = request.user
        todo.save()
        messages.add_message(request,messages.SUCCESS, "Created Successfully"
        
        )

        return HttpResponseRedirect(reverse("todo_detail",kwargs={'id':todo.pk}))



    return render(request,'todo/create_todo.html', context)

@login_required
def todo_detail(request,id):
    todo = get_object_or_404(Todo,pk=id)
    context = {'todo':todo}
    return render(request,'todo/todo_detail.html',context)

@login_required
def todo_delete(request,id):
    todo = get_object_or_404(Todo,pk=id)
    context = {'todo':todo}
    if request.method == 'POST':
        todo.delete()
        messages.add_message(request,messages.WARNING, "DEleted Successfully"
        
        )
        return HttpResponseRedirect(reverse('home'))

    return render(request,'todo/todo_delete.html',context)