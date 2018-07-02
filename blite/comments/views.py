from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Comment
from blog.models import Post
from django.views import View
from .forms import CommentForm, UpdateCommentForm, DeleteCommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.core.exceptions import FieldError # for querystring
# Create your views here.

class CommentController(View):

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and request.POST.get("HTTP_method"): # only PUT/DELETE HAVE HTTP_method field
            request.method = request.POST["HTTP_method"] 
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, comment_id): # dispatcher or url_router supplies comment_id (==None) even though it is not needed for POST
        # comment_id is in this case used for post_id !!!!!!!!!!
        post = Post.objects.get(id=comment_id)
        comment_form = CommentForm({"title":request.POST['title'], "content":request.POST['content']})
        if comment_form.create_save(request.user, post):
            return redirect('blog:post_controller')
        return render(request, 'main/error.html', {"error": "400"}, status=400) # bad form request

    @method_decorator(login_required)
    def put(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        if comment.has_owner(request.user) or request.user.is_superuser: # check if user created this comment, or if user is admin
            comment_form = UpdateCommentForm(request.POST, instance=comment) # specifying the instance we supply PK - django can resolve UPSERT
            if comment_form.is_valid(): # django abstracts UPSERT away, you always just .save()
                comment_form.save()
                return redirect('blog:post_controller')
            return render(request, 'main/error.html', {"error": "400"}, status=400) # not authorized to modify resource
        return render(request, 'main/error.html', {"error": "403"}, status=403) # not authorized to modify resource

    @method_decorator(login_required)
    def delete(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        if comment.has_owner(request.user) or request.user.is_superuser: # user can only delete his own instances (admin can delete anything)
            if request.POST.get('confirmation', None) == "YES": # check if confirmation checkbox was marked
                comment.delete() # actually delete
                return redirect('blog:post_controller')
            return render(request, 'main/error.html', {"error": "400"}, status=400) ## not authorized to modify resource
        return render(request, 'main/error.html', {"error": "403"}, status=404) # bad form request

@login_required
def create_comment(request, post_id): # just render the comment_create_form html
    if post_id:
        return render(request,'comments/comment_create_form.html' , { "form": CommentForm, "post_id": post_id })
    return render(request, 'main/error.html', {"error": "400"}, status=400) # bad form request

@login_required
def edit_comment(request, comment_id): # just render the comment_edit_form html
    comment = Comment.objects.get(id=comment_id)
    form = UpdateCommentForm(instance=comment) # populate the form either with request.POST data, or with instance data
    return render(request,'comments/comment_edit_form.html' ,{"form":form, "comment_id": comment_id})

@login_required
def delete_comment(request, comment_id): # just render the comment_delete_form html
    return render(request,'comments/comment_delete_form.html', {"form": DeleteCommentForm, "comment_id": comment_id})