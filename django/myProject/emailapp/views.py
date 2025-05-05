from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    emailObj = {
        'title': 'Cong ty Hieu Tran',
        'description': 'Thong bao lich phong van',
        'date': 'Hom qua'
    }
    return render(request, 'home.html', {'emailObj': emailObj})