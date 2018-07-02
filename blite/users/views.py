from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserProfileForm, UserUpdateForm, UserDeleteForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class UserController(View):

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and request.POST.get("HTTP_method"): # only PUT/DELETE HAVE HTTP_method field
            request.method = request.POST["HTTP_method"] 
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def put(self, request, user_id): # update user
        if request.user.is_superuser or request.user.id == int(user_id):
            userform = UserUpdateForm(request.POST, instance=request.user) # specifying the instance we supply PK - django can resolve UPSERT
            if userform.is_valid(): # django abstracts UPSERT away, you always just .save()
                userform.save()
                return redirect('users:profile', user_id=user_id)
            return render(request, 'main/error.html', {"error": "400"}, status=400)
        return render(request, 'main/error.html', {"error": "403"}, status=403) 

    @method_decorator(login_required)
    def delete(self, request, user_id): # delete user
        if request.user.is_superuser or request.user.id == int(user_id):
            if request.POST.get('confirmation', None) == "YES":
                request.user.delete() # actually delete
                return redirect('blog:post_controller')
            return render(request, 'main/error.html', {"error": "400"}, status=400) 
        return render(request, 'main/error.html', {"error": "403"}, status=403) 


def register(request): # POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:post_controller')
        return render(request, 'users/register.html', { "form": form}, status="400")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', { "form": form} )

def login_handler(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) # keyword 'data' IS IMPORTANT, otherwise form.is_valid == False
        if form.is_valid():
            user = form.get_user() # AuthtenticationForm provides this function to derive the user
            login(request, user) # login, create a cookie
            return redirect('blog:post_controller')
        return render(request, 'users/login.html', { "form": form}, status="400")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', { "form": form})

def logout_handler(request):
    if request.method == "POST": # yes POST is the best practice for logout
        logout(request) # yes request, not request.user - check django docs
        return redirect('blog:post_controller')
    return render(request, 'main/error.html', {"error": "405"}, status="405") # get method not allowed

@login_required
def profile(request, user_id):
    if not request.user.is_superuser:
        if request.user.id != int(user_id): 
            return render(request, 'main/error.html', {"error": "400"}, status=400)
    user = User.objects.get(id=user_id)
    return render(request, 'users/profile.html', { "main_item": user})

# check if user logged in or admin
# check if all/published/private requested
# paginate results
@login_required
def user_posts(request, user_id, filter):
    if not request.user.is_superuser:
        if request.user.id != int(user_id):
            return render(request, 'main/error.html', {"error": "400"}, status=400)
    user = User.objects.get(id=user_id)
    user_posts = user.post_set.custom_filter(filter).paginated(request.GET.get('page'), 3)
    return render(request, 'users/profile.html', { "main_item": user, "items": user_posts })

@login_required
def edit_user(request, user_id): # just render the post_edit_form html
    user = User.objects.get(id=user_id)
    form = UserUpdateForm(instance=user) # populate the form either with request.POST data, or with instance data
    return render(request,'users/user_edit_form.html' ,{"form":form, "user_id":user_id})

@login_required
def delete_user(request, user_id): # just render the post_delete_form html
    return render(request,'users/user_delete_form.html', {"form": UserDeleteForm, "user_id":user_id})
