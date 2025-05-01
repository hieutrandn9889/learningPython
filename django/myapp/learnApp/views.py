from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def static(request):
    return render(request, 'static.html', {'title': 'Welcome to MyApp'})

def variable(request):
    context = {
        'username': 'John Doe',
        'age': 30,
        'email': 'john.doe@example.com',
        'hobbies': ['Reading', 'Traveling', 'Cooking'],
    }
    return render(request, 'variable.html', context)

def counterGETInput(request):
    text = request.GET.get('text', '')
    word_list = text.split() if text else []
    word_count = len(word_list)
    return render(request, 'counterGETInput.html', {'word_count': word_count})

def GETTextarea(request):
    text = request.GET['text']
    word_list = text.split() if text else []
    word_count = len(word_list)
    return render(request, 'GETTextarea.html', {'word_count': word_count})

def POSTTextarea(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')  # Safely get 'text' with a default value
    else:
        text = ''  # Default value if the request is not POST
    word_list = text.split() if text else []
    word_count = len(word_list)
    return render(request, 'POSTTextarea.html', {'word_count': word_count})