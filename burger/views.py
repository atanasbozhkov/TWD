from django.http import HttpResponse

def index(request):
    return HttpResponse("Burger says hey hunger game!")