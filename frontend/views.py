from django.shortcuts import render

# Create your views here.
def frontend(request):
    return render(request, 'index.html', {})