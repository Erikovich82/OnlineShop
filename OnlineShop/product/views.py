# from django.shortcuts import render

from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    # return render(request, 'h/index.html')
   return HttpResponse('<h1> product index </h1>')