from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from .forms import CheckPasswordForm
from main.models import Post, Comment, Recomment
from accounts.models import BlazeUser

def mypage(request):
    user = request.user
    nickname = user.nickname
    email = user.email
    country = user.country
    return render(request,'mypage.html',{'nickname':nickname,'email':email,'country':country})

def mypageBlaze(request):
    user = request.user
    id = request.user.id
    email = request.user.email
    blazes = user.likes.all()
    # if user in like_users:
    return render(request,'mypageBlaze.html',{'blazes':blazes})

def mypagePosts(request):
    email = request.user.email
    id=request.user.id
    posts = Post.objects.all()
    post_list = posts.filter(author=id) # 내가 쓴글만
    # blog_list = Blog.objects.all().order_by('-id') # 블로그 객체 다 가져오기
    return render(request, 'mypagePosts.html', {'post_list':post_list})

def mypageComments(request):
    user = request.user
    id=request.user.id
    comments = Comment.objects.all()
    comment_list = comments.filter(user_id=id)
    recomments = Recomment.objects.all()
    recomment_list = recomments.filter(user_id=id)
    return render(request,'mypageComments.html', {'comment_list':comment_list,'recomment_list':recomment_list})

def go_editNickname(request):
    return render(request,'editNickname.html')

def editNickname(request):
    if request.method == "POST":
        user = request.user
        user.nickname = request.POST["nickname"]
        user.save()
        return redirect('mypageapp:mypage')
    return render(request,'mypage.html')

def signout(request):
    if request.method == "POST":
        pw_del = request.POST["pw_del"]
        user = request.user
        password = user.password
        if pw_del == password:
            user.delete()
            return redirect('main:main')
    return render(request, 'signout.html')

def profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)
        
        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "Sign Out has been completed.")
            return redirect('/intro/index/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'signout.html', {'password_form':password_form})
