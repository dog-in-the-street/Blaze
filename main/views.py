from django.db import models
from django.db.models import fields
from django.forms.models import construct_instance
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
# from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.detail import DetailView
from .models import Category, Images, Post, Message
from .forms import ImageForm, PostForm
from django.forms import modelformset_factory
from django.contrib.auth.models import User

import flag

from django.core.paginator import Paginator

def main(request):
    context = dict()
    all_post = Post.objects.all()
    context['all_post'] = all_post
    flag = request.user.country
    context['flag'] = flag
    print(flag.flag)
    categories = Category.objects.all()
    context['categories'] = categories
    return render(request,'main.html',context)

def create(request):
    # 하나의 modelform 을 여러번 쓸 수 있음. 모델, 모델폼, 몇 개의 폼을 띄울건지 갯수 
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=5)
   
    if request.method == 'POST':
        
        postForm = PostForm(request.POST)
        # queryset 을 none 으로 정의해서 이미지가 없어도 되도록 설정. none 은 빈 쿼리셋 리턴
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())
    
        # 두 모델폼의 유효성 검사를 해주고
        if postForm.is_valid() and formset.is_valid():
            # 저장을 잠시 멈추고
            post_form = postForm.save(commit=False)
            # Post user 에 현재 요청된 user 를 담아서 
            post_form.author = request.user
            # 저장. 이 작업 안하면 user null error
            post_form.save()
            # 유효성 검사가 왼료된 formset 정리된 데이터 모음
            for form in formset.cleaned_data:
               
                if form:
                    # image file 
                    image = form['image']
                    # post, image file save
                    photo = Images(post=post_form, image=image)
                    photo.save()
            
            return redirect('main')
        # 유효성 검사 실패시 에러메세지를 터미널상에 print
        else:
            print(postForm.errors, formset.errors)
    else:
        # POST 요청이 아닌 경우 
        postForm = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    
    return render(request, 'post/create.html',
                  {'postForm': postForm, 'formset': formset})


# def create(request):
#     create_form = PostForm(request.POST)
#     ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=5)

#     if request.method =="POST":
#         create_form = PostForm(request.POST,request.FILES)

#         formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
#         if create_form.is_valid() and formset.is_valid():
#             temp_form = create_form.save(commit=False)
#             temp_form.author = request.user
#             temp_form.save()

#             for form in formset.cleaned_data:

#                 if form:
#                     image = form['image']
#                     photo = Images(post=temp_form, image=image)
#                     photo.save()

#             return redirect('main')
#     else:
#         create_form = PostForm()
#         formset = ImageFormSet(queryset=Images.objects.none())


#     return render(request,'post/create.html',{'create_form':create_form, 'ImageFormSet': ImageFormSet})


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


def category(request,category_id):
    context = dict()
    category = Category.objects.get(id=category_id) 
    category_post = Post.objects.filter(category=category).order_by('-id')
    context['category_post']  =category_post   
   
    return render(request,'category/post_list.html',context)
    
  

# chat
def lobby(request):
    # 나와 채팅한 유저가 최신순으로 채팅방 리스트에 정렬되어야 함. 
    # 해당 메시지에서 연결된 foreignkey를 참조하면 됨. 
    # 메시지를 순차적으로 정렬
    # 한 명 당 여러 개의 메시지가 들어올 수 있는데 이 중에서 하나를 받아오면 나머지는 무시하고 다음 유저로. 

    # Message
    messages = Message.objects.all()

    # User
    users = User.objects.all() # 나중에 수정하기
    return render(request, 'chat/lobby.html', {
        'users' : users,
        'messages' : messages,
    })


def room(request, room_name):
    recent_messages = Message.objects.filter(room=room_name).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room_name' : room_name,
        'recent_messages' : recent_messages,
    })






