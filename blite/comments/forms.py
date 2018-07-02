from django import forms
from .models import Comment
from blog.models import Post


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['title', 'content']

    def create_save(self, user, post):
        if self.is_valid(): # already instantiated with the data
            if post.published: # you can only add comments to published posts!
                comment_instance = self.save(commit=False)
                comment_instance.author = user
                comment_instance.post = post
                comment_instance.save()
                return True
        return False


class UpdateCommentForm(CommentForm): # this one inherits from the CommentForm

    HTTP_method = forms.CharField(initial="PUT", widget=forms.HiddenInput())


class DeleteCommentForm(forms.Form): # this one does not inherit from modelForm, just a basic form
    
    CONFIRMATION_CHOICES = (('NO', 'NO'), ('YES', 'YES'))

    HTTP_method = forms.CharField(initial="DELETE", widget=forms.HiddenInput())
    confirmation = forms.ChoiceField(choices = CONFIRMATION_CHOICES,
                                initial='NO',
                                widget=forms.Select(),
                                required=True)

