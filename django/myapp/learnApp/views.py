from django.shortcuts import render
from django.http import HttpResponse
from .models import Feature

# Create your views here.
def index(request):
    feature1 = Feature()
    feature1.id = 0
    feature1.name = 'Fast'
    feature1.details = 'Our service is very quick'
    feature2 = Feature()
    feature2.id = 1
    feature2.name = 'Fast'
    feature2.details = 'Our service is very quick'
    feature3 = Feature()
    feature3.id = 2
    feature3.name = 'Innovative'
    feature3.details = 'We provide innovative solutions'
    feature4 = Feature()
    feature4.id = 2
    feature4.name = 'Innovative'
    feature4.details = 'We provide innovative solutions'
    return render(request, 'index.html', {'feature1': feature1, 'feature2': feature2, 'feature3': feature3, 'feature4': feature4})

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