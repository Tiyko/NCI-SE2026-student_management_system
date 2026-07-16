from django.shortcuts import render


# Create your views here.
def index(request):
    # Render the home page template
    # return HttpResponse("HOME PAGE OK")
    return render(request, 'home/index.html')
