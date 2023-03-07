from django import forms
from my_blog.models import Post, Comment

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('author', 'title', 'text')
    
    #adding a widget to connect to css for editing using the class
    widget = {
      'title': forms.TextInput(attrs={'class':'textinputclass'}),
      'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}) 
    }

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('author', 'text')
    widget = {
      'author': forms.TextInput(attrs={'class':'textinputclass'}),
      'text' : forms.Textarea(attrs={'class':'editable medium-editor-textarea'}), 
    }