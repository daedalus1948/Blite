from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from django.urls import reverse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # for pagination
# Create your models here.


class CommentQuerySetAsManager(models.QuerySet): # same paginator code as posts
    
    def paginated(self, page, per_page=3):
        posts = self.order_by('-create_date')
        paginator = Paginator(posts, per_page)
        try:
            paginated_posts = paginator.page(page) # querystring page
        except PageNotAnInteger: # not a number? return first page (missing parameter, or wrong keyword)
            paginated_posts = paginator.page(1)
        except EmptyPage: # number higher than pages? return last page
            paginated_posts = paginator.page(paginator.num_pages)
        return paginated_posts


class Comment(models.Model):

    author = models.ForeignKey(User, default=None, null=False)
    post = models.ForeignKey(Post, default=None, null=False)
    
    title = models.CharField(max_length=80, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    update_date = models.DateTimeField(auto_now_add=True, blank=True)
    
    # custom queryset manager
    comments = CommentQuerySetAsManager.as_manager() # paginated
    objects = models.Manager() # default manager

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('comments:comment_controller', kwargs={"comment_id": self.id})

    def get_edit_url(self):
        return reverse('comments:edit_comment', kwargs={"comment_id": self.id})

    def get_delete_url(self):
        return reverse('comments:delete_comment', kwargs={"comment_id": self.id})

    def has_owner(self, user):
        if user.id != self.author.id:
            return False
        return True
