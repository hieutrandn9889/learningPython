from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.utils.formats import number_format


from .models import Course
from .models import price_course  


# Create your views here.
def index(request):
        courses = Course.objects.all()  # Fetch all Course objects from the database
        PriceCourses = price_course.objects.all()  # Fetch all PriceCourses objects from the database
        return render(request, 'index.html', {'courses': courses, 'PriceCourses': PriceCourses})

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
            messages.error(request, 'Mật khẩu không khớp.')
            return render(request, 'register.html')

        # Password validation
        if len(password) < 8:
            messages.error(request, 'Mật khẩu của bạn phải chứa ít nhất 8 ký tự.')
            return render(request, 'register.html')

        if password.isdigit():
            messages.error(request, 'Mật khẩu của bạn không thể hoàn toàn là số.')
            return render(request, 'register.html')

        if username.lower() in password.lower() or email.lower() in password.lower():
            messages.error(request, 'Mật khẩu của bạn không thể quá giống thông tin cá nhân khác.')
            return render(request, 'register.html')

        # Check if the password is commonly used
        common_passwords = ['password', '123456', '12345678', 'qwerty', 'abc123', 'password1']
        if password.lower() in common_passwords:
            messages.error(request, 'Mật khẩu của bạn không thể là mật khẩu thường dùng.')
            return render(request, 'register.html')

        # Create and save the user
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'Người dùng đã đăng ký thành công! Bạn có thể đăng nhập.')
            return render(request, 'login.html')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'register.html')

    # Render the registration form for GET requests
    return render(request, 'register.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            auth_login(request, user)
            messages.success(request, 'Bạn đã đăng nhập thành công.')
            return redirect('index')  # Redirect to the home page or dashboard
        else:
            # Invalid credentials
            messages.error(request, 'Tài khoản hoặc mật khẩu không đúng.')
            return render(request, 'login.html')

    # Render the login form for GET requests
    return render(request, 'login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        # Check if the email exists in the database
        try:
            user = User.objects.get(email=email)
            # Generate a reset link (for simplicity, just a placeholder here)
            reset_link = f"http://127.0.0.1:8000/reset-password/{user.id}/"

            # Send the reset link via email
            send_mail(
                'Mật khẩu mới của bạn',
                f'Hi {user.username},\n\nClick the link below to reset your password:\n{reset_link}',
                'admin@myapp.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Mật khẩu mới của bạn đã được gửi qua email. Vui lòng kiểm tra hộp thư đến của bạn.')
        except User.DoesNotExist:
            messages.error(request, 'Không tìm thấy tài khoản với email đó.')

        return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')

def logout(request):
    auth_logout(request)  # Log the user out
    messages.success(request, 'Bạn đã đăng xuất thành công.')
    return redirect('index')  # Redirect to the login page

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, 'course_detail.html', {'course': course})

def about(request):
    return render(request, 'about.html')

def courses(request):
    return render(request, 'courses.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def team(request):
    return render(request, 'team.html')

def contact(request):
    return render(request, 'contact.html')

def price_course_detail(request):
    return render(request, 'price_course_detail.html')