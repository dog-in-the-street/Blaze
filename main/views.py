from django.db import models
from django.db.models import fields
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaultfilters import time
from .models import *
from .forms import *
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import flag
from datetime import date, timedelta

def main(request):
    context = dict()

    all_post = Post.objects.all().order_by('-id')
    context['all_post'] = all_post
    categories = Category.objects.all()
    context['categories'] = categories
   
    
    return render(request,'main.html',context)

@login_required(login_url="/signin/")
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


def detail(request,post_id):
    context = dict()
    
    my_post = get_object_or_404(Post, id=post_id)
    context['my_post'] = my_post
    comment_form = CommentForm()
    context['comment_form'] = comment_form
    recomment_form = RecommentForm()
    context['recomment_form'] = recomment_form

    return render(request,'post/detail.html',context)






@login_required(login_url="/signin/")
def delete(request,post_id):
    my_post = get_object_or_404(Post, id=post_id)
    my_post.delete()
    return redirect('main')


def category(request,category_id):
    context = dict()
    categories = Category.objects.all()
    context['categories'] =categories
    category = Category.objects.get(id=category_id) 
    category_post = Post.objects.filter(category=category).order_by('-id')
    context['category_post']  =category_post   
   
    return render(request,'category/post_list.html',context)



@login_required(login_url="/signin/")
def create_comment(request,post_id):
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        temp_form = comment_form.save(commit=False)
        temp_form.post = Post.objects.get(id=post_id)
        temp_form.user = request.user
        temp_form.save()
        return redirect('detail',post_id)
    else:
        comment_form = CommentForm()
        print("request error")

    return redirect('detail',post_id)



@login_required(login_url="/signin/")
def delete_comment(request,com_id,post_id):
    my_com = get_object_or_404(Comment,id=com_id)
    my_com.delete()
    return redirect('detail',post_id)

@login_required(login_url="/signin/")
def create_recomment(request,recom_id,post_id):
    my_post = get_object_or_404(Post,id=post_id)
    my_com = get_object_or_404(Comment,id=recom_id)
    if request.method =="POST":
        recom_form = RecommentForm(request.POST)
        temp_form = recom_form.save(commit=False)
        temp_form.post = my_post
        temp_form.comment = my_com 
        temp_form.user = request.user
        temp_form.save()
        return redirect('detail',post_id)
    else:
        recom_form = RecommentForm()

    return redirect('detail',post_id)




@login_required(login_url="/signin/")
def delete_recomment(request,recom_id,post_id):
    my_recom = get_object_or_404(Recomment,id=recom_id)
    my_recom.delete()
    return redirect('detail',post_id)

def search(request):
    context = dict()
    post = request.POST.get("post","")
    categories = Category.objects.all()
    context['categories'] = categories
    if post:
        search_post = Post.objects.filter(title__icontains=post)| Post.objects.filter(text__icontains=post).order_by('-id')
        context['search_post']=search_post
        context['post']=post
        return render(request, 'post/search.html', context)
    else:
        return render(request, 'post/search.html',context)
  
  
# chat
@login_required(login_url="/signin/")
def lobby(request):
    # 기본 유저 정보
    context = dict()
    user_flag = flag.flag("KR")
    context['flag'] = user_flag
    
    # chatroom list
    # 현재 로그인한 유저
    logged_user = request.user
    context['logged_user'] = logged_user

    # through
    chatroom_lists = ChatRoomUser.objects.filter(user=logged_user) # 객체 자체를 가져오는 것.
    context['chatroom_lists'] = chatroom_lists

    # 날짜 계산
    today = date.today()
    yesterday = date.today() - timedelta(1)
    context['today'] = today
    context['yesterday'] = yesterday
    
    
    return render(request, 'chat/lobby.html', context)


@login_required(login_url="/signin/")
def room(request, room_name):
    context = dict()
    recent_messages = Message.objects.filter(room=room_name).order_by('timestamp')
    # 현재 로그인한 유저
    logged_user = request.user
    context['logged_user'] = logged_user
    
    context['room_name'] = room_name
    context['recent_messages'] = recent_messages


    return render(request, 'chat/room.html', context)


@login_required(login_url="/signin/")
def like(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    user = request.user
    if user in post.like_users.all():
        post.like_users.remove(user)
        liked = False
        print(liked)
    else:
        post.like_users.add(user)
        liked = True
        print(liked)
    context = {
        'liked':liked,
        'count':post.like_users.count()
    }

    return JsonResponse(context)

@login_required
def goMypage(request):
    return render(request,'mypageapp:mypage')

def best_topic(request):
    week_post = Post.objects.filter(registered_date__iso_week_day__gte=1).order_by('-like_users','-id')
    ranking = week_post[0:10]
    categories = Category.objects.all()
    return render(request,'post/best-topic.html',{'ranking':ranking,'categories': categories})