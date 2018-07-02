from django.shortcuts import render
 
 
def error_404(request):
        return render(request,'main/error.html', {"error": 404})
 
def error_500(request):
        return render(request,'main/error.html', {"error": 500})