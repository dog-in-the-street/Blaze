from django.db import models
from django.db.models import fields
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
# from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.detail import DetailView
from .models import Images, Post
from .forms import ImageForm, PostForm
from django.forms import modelformset_factory

def main(request):
    all_post = Post.objects.all()
    return render(request,'main.html',{'all_post': all_post})

def create(request):
    create_form = PostForm(request.POST)
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=5)

    if request.method =="POST":
        create_form = PostForm(request.POST,request.FILES)

        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        if create_form.is_valid() and formset.is_valid():
            temp_form = create_form.save(commit=False)
            temp_form.author = request.user
            temp_form.save()

            for form in formset.cleaned_data:

                if form:
                    image = form['image']
                    print(form)
                    print(form['image'])
                    photo = Images(post=temp_form, image=image)
                    photo.save()

        return redirect('main')
    else:
        create_form = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())


    return render(request,'post/create.html',{'create_form':create_form, 'ImageFormSet': ImageFormSet})


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


# def All(request):
#     context = dict()
#     if request.method == "POST" :
#         field_form = PostForm(request.POST, request.FILES)
#         if field_form.is_valid():
#             temp_form = field_form.save(commit = False)
#             temp_form.category = "All"
#             temp_form.save()
#         return redirect('all')
#     context['post_form'] = PostForm()
#     return render(request,'create.html',context)

# def Hotplace(request,category_id):
    
#     return render('category/Hotplace.html')

# def Univlife(request):
#     context = dict()
#     if request.method == "POST" :
#         field_form = PostForm(request.POST, request.FILES)
#         if field_form.is_valid():
#             temp_form = field_form.save(commit = False)
#             temp_form.category = "Univ life"
#             temp_form.save()
#         return redirect('univlife')
#     context['post_form'] = PostForm()
#     return render(request,'create.html',context)

# def Languageexchange(request):
#     context = dict()
#     if request.method == "POST" :
#         field_form = PostForm(request.POST, request.FILES)
#         if field_form.is_valid():
#             temp_form = field_form.save(commit = False)
#             temp_form.category = "Language exchange"
#             temp_form.save()
#         return redirect('languageexchange')
#     context['post_form'] = PostForm()
#     return render(request,'create.html',context)

# def K_culture(request):
#     context = dict()
#     if request.method == "POST" :
#         field_form = PostForm(request.POST, request.FILES)
#         if field_form.is_valid():
#             temp_form = field_form.save(commit = False)
#             temp_form.category = "All"
#             temp_form.save()
#         return redirect('all')
#     context['post_form'] = PostForm()
#     return render(request,'create.html',context)


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


