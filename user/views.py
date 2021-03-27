from django.shortcuts import render, redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from article.models import Article
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
        
    form = RegisterForm(request.POST or None)
    if form.is_valid():

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        
        login(request,newUser)
        messages.success(request,"Kayıt Başarıyla Gerçekleşti")
        
        return redirect("index")
           
    context = {
                    "form": form
                }
    return render(request, "register.html", context)
        


def loginUser(request):
    form = LoginForm(request.POST or None)
    
    context = {
        "form" : form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password = password)
        if user is None:
            messages.info(request,"Kullanıcı Adı Veya Şifre Hatalı")
            return render(request,"login.html",context)
        
        messages.success(request,"Başarılı Giriş")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)
@login_required(login_url = "user:loginUser")    
def logoutUser(request):

    logout(request)
    messages.success(request,"Başarılı Çıkış")
    return redirect("index")
@login_required(login_url = "user:loginUser")
def deneme(request):
    articles = Article.objects.filter(author = request.user)
    content = {
        "articles" : articles
    }
    return render(request,"editprofile.html",content)