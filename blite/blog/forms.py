from django import forms
from . import models

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post

        fields = ['title', 'content', 'picture', 'published']

    #custom validation
    def clean(self):
        print("overriding clean function on PostForm ModelForm - testing ")
        super().clean() # call the superclass clean as always

    def create_and_persist(self, user=None):
        if self.is_valid(): # custom sanitize if needed - is valid is true even if required fields are empty
            # remember postform_object != post_object !!!
            post_instance = self.save(commit=False) # form upon save with commit=false returns the actual post_instance
            post_instance.author = user # if user parameter supplied, update form, else persist without change
            post_instance.save()
            return True
        return False

# HTML 5 FORMS DO NOT SUPPORT PUT/DELETE (ONLY XHR/AJAX DOES) THEREFORE
# these two forms include a hidden field for method="PUT" and method="DELETE"
# modify the class-based-view Post-CRUD controller dispatch method to reroute these forms to
# PUT and DELETE CONTROLLERS/methods

class UpdatePostForm(PostForm): # inherits from the PostForm

    HTTP_method = forms.CharField(initial="PUT", widget=forms.HiddenInput())

class DeletePostForm(forms.Form): # does not inherit from ModelForm, just a basic form
    
    CONFIRMATION_CHOICES = (('NO', 'NO'), ('YES', 'YES'))

    HTTP_method = forms.CharField(initial="DELETE", widget=forms.HiddenInput())
    confirmation = forms.ChoiceField(choices = CONFIRMATION_CHOICES,
                                initial='NO',
                                widget=forms.Select(),
                                required=True)

