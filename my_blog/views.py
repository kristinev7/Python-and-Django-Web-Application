from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from my_blog.models import Post, Comment
from my_blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy  #waits until the post has been deleted to return success_url

# Class based views


class AboutView(TemplateView):
    template_name = 'about.html'


#home page
class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(
            published_date__lte=timezone.now()).order_by('-published_date')
        #lte = 'less than or equal to' so grab posts lte of the user's timezone and order it by date
        # '-'published_date: order the result in descending order


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'  #if user is not login redirect them to login
    redirect_field_name = 'my_blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'my_blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'my_blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(
            published_date__isnull=True).order_by('created_date')


###########################################
#functions
##########################################
#publish post
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk)


#get user comments for a post
@login_required  #require user to be logged in to leave a comment
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
      form = CommentForm(request.POST)
      if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('post_detail', pk=post.pk)
      else:
        form = CommentForm()
        return render(request, 'my_blog/comment_form.html', {'form': form})

#commend approval
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk  #save the comment pk to another variable so we dont lose it
    comment.delete()
    return redirect('post_detail', pk=post_pk)
