from django.db import models
from django.db.models import fields
from django.shortcuts import get_object_or_404, render, redirect
# from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.detail import DetailView
from .models import Post
from .forms import PostForm

def main(request):
    all_post = Post.objects.all()
    return render(request,'main.html',{'all_post': all_post})

def create(request):
    if request.method =="POST":
        create_form = PostForm(request.POST,request.FILES)
        if create_form.is_valid():
            temp_form = create_form.save(commit=False)
            temp_form.author = request.user
            temp_form.save()
        return redirect('main')
    post_form = PostForm
    return render(request,'post/create.html',{'post_form':post_form})


def detail(request,post_id):
    my_post = get_object_or_404(Post, id=post_id)
    return render(request,'post/detail.html',{'my_post':my_post})

def update(request,post_id):
    my_post = get_object_or_404(Post,id=post_id)
    if request.method == "POST":
        update_form = PostForm(request.POST,instance=my_post)

        if update_form.is_valid():
            update_form.save()
            return redirect('main')

    update_form = PostForm(instance=my_post)
    return render(request,'post/update.html',{'update_form':update_form})

def delete(request,post_id):
    my_post = get_object_or_404(Post, id=post_id)
    my_post.delete()
    return redirect('main')



# class PostList(ListView):
#     model = Post
#     template_name_suffix = '_list'

# class PostCreate(CreateView):
#     model = Post
#     fields = ['text', 'image']
#     template_name_suffix = ' _create' #로그인 한 사람만
#     success_url = '/'

# class PostUpdate(UpdateView):
#     model = Post
#     fields = ['text','image']
#     template_name_suffix = '_update'
#     success_url = '/'

# class PostDelete(DeleteView):
#     model = Post
#     template_name_suffix = '_delete'
#     success_url = '/'


# class PostDetail(DetailView):
#     model = Post
#     template_name_suffix = '_detail'
#     success_url = '/'
