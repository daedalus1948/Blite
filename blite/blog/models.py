from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # for pagination

# create a custom QuerySet and call it .as_manager() on model
# since this way the queryset still retains method chaining
class PostQuerySetAsManager(models.QuerySet): 
    
    def published(self):
        return self.filter(published=True)

    def private(self):
        return self.filter(published=False)

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

    def custom_filter(self, filter): # filter 
        if filter: # if filter = None, return the whole queryset
            if filter=="published":
                return self.published()
            if filter=="private":
                return self.private()
        return self.all()


class Post(models.Model):
    
    title = models.CharField(max_length=80, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    picture = models.FileField(null=True, blank=True, upload_to='media/images') # store links to images in media folder, blank is for forms

    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    update_date = models.DateTimeField(auto_now_add=True, blank=True)
    published = models.BooleanField(default=0, null=False)
    
    author = models.ForeignKey(User, default=None, null=False)

    # custom managers
    posts = PostQuerySetAsManager.as_manager() # paginated
    objects = models.Manager() # default manager


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_controller', kwargs={"post_id": self.id})

    def get_edit_url(self):
        return reverse('blog:edit_post', kwargs={"post_id": self.id})

    def get_delete_url(self):
        return reverse('blog:delete_post', kwargs={"post_id": self.id})

    def save(self, *args, **kwargs):
        print("running a custom overriden save on Post Model - testing")
        super().save() # run the superclass usual save afterwards

    # custom method - row-level-based-permission to check if user can operate on instance created by him
    def has_owner(self, user):
        if user.id != self.author.id:
            return False
        return True




