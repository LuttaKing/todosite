from django.shortcuts import render

def handle_404n(request,exception):

    return render(request,'not_found.html')

def handle_500(request):
    
    return render(request,'not_found.html')