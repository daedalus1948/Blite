from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from django.views import View
from .forms import PostForm, UpdatePostForm, DeletePostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import FieldError # for querystring
from .utils import build_Q_dictionary

#class based views  - inherit from View !!!!! (the simplest base case)
class PostController(View): # this is a classic CRUD/REST-like controller
    # override dispatch so it calls appropiate controllers based on the form "HTTP_method"
    # hidden field for "PUT" and "DELETE" cases since HTML5 forms do not support other methods 
    # than GET/POST
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and request.POST.get("HTTP_method"): # only PUT/DELETE HAVE HTTP_method field
            request.method = request.POST["HTTP_method"] 
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        if post_id: # if post_id present - fetch a post by id else fetch all posts (REST-like)
            post = Post.posts.published().get(id=post_id) # since get is not iterable whereas filter is
            comments = post.comment_set.all().paginated(request.GET.get('page'), 3)
            return render(request, 'blog/post_detail.html', {"main_item": post, "items": comments, "add_comment": True})
        else: # show all results, preferably paginated
            posts = Post.posts.published().paginated(request.GET.get('page'), 3)
        return render(request, 'blog/posts.html', {"items":posts})

    @method_decorator(login_required)
    def post(self, request, post_id): # dispatcher or url_router supplies post_id (==None) even though it is not needed for POST
        postform = PostForm(request.POST,request.FILES)
        if postform.create_and_persist(request.user): # custom sanitize if needed
            return redirect('blog:post_controller')
        return render(request, 'main/error.html', {"error": "400"}, status=400) # bad form request

    @method_decorator(login_required)
    def put(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post.has_owner(request.user) or request.user.is_superuser: # check if user created this post, or if user is admin
            postform = UpdatePostForm(request.POST, request.FILES, instance=post) # specifying the instance we supply PK - django can resolve UPSERT
            if postform.create_and_persist(request.user): # django abstracts UPSERT away, you always just .save()
                return redirect('blog:post_controller')
            return render(request, 'main/error.html', {"error": "400"}, status=400) # bad form request
        return render(request, 'main/error.html', {"error": "403"}, status=403) # not authorized to modify resource

    @method_decorator(login_required)
    def delete(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if post.has_owner(request.user) or request.user.is_superuser: # user can only delete his own instances (admin can delete anything)
            if request.POST.get('confirmation', None) == "YES": # check if confirmation checkbox was marked
                post.delete() # actually delete
                return redirect('blog:post_controller')
            return render(request, 'main/error.html', {"error": "400"}, status=400) # bad form request
        return render(request, 'main/error.html', {"error": "403"}, status=403) # not authorized to modify resource

@login_required
def create_post(request): # just render the post_create_form html
    return render(request,'blog/post_create_form.html' ,{ "form": PostForm })

@login_required
def edit_post(request, post_id): # just render the post_edit_form html
    post = Post.objects.get(id=post_id)
    form = UpdatePostForm(instance=post) # populate the form either with request.POST data, or with instance data
    return render(request,'blog/post_edit_form.html' ,{"form":form, "post_id": post_id})

@login_required
def delete_post(request, post_id): # just render the post_delete_form html
    return render(request,'blog/post_delete_form.html', {"form": DeletePostForm, "post_id": post_id})

def search_post(request): # receives a query string with various key-value attributes for search
    Q_dict = build_Q_dictionary(request.GET.dict()) # supply python dictionary generated from the querystring
    try: # querystring may contain unresolvable keywords
        searched_posts = Post.posts.published().filter(Q_dict).paginated(request.GET.get('page'), 3)
    except FieldError: # if wrong keyword, return all posts
        searched_posts = Post.posts.published().paginated(request.GET.get('page'), 3)    
    return render(request, 'blog/posts.html', {"items": searched_posts })
