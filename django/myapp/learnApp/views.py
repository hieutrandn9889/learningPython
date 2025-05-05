from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Feature


# Create your views here.
def index(request):
        features = Feature.objects.all()  # Fetch all Feature objects from the database
        return render(request, 'index.html', {'features': features})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        email = request.POST.get('email', '').strip()

        # Check if email or username already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')
        
        # Validate password and confirmation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')  

        # Password validation
        if len(password) < 8:
            messages.error(request, 'Your password must contain at least 8 characters.')
            return render(request, 'register.html')

        if password.isdigit():
            messages.error(request, 'Your password can’t be entirely numeric.')
            return render(request, 'register.html')

        if username.lower() in password.lower() or email.lower() in password.lower():
            messages.error(request, 'Your password can’t be too similar to your other personal information.')
            return render(request, 'register.html')

        # Check if the password is commonly used
        common_passwords = ['password', '123456', '12345678', 'qwerty', 'abc123', 'password1']
        if password.lower() in common_passwords:
            messages.error(request, 'Your password can’t be a commonly used password.')
            return render(request, 'register.html')

        
        # Create and save the user
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'User registered successfully! You can now log in.')
            return render(request, 'login.html')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'register.html')

    # Render the registration form for GET requests
    return render(request, 'register.html')















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