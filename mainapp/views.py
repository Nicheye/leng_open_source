from django.shortcuts import render,redirect
from django.contrib.auth.models import  User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import table as Table

from django.db.models import Q
from .models import Profile,FeedBack
from .models import word as Word
from .models import Follow
from .forms import SignUpForm,TableForm,WordForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from random import choice
# Create your views here.
def main(request):
    #getting user and put them in paginator
    users = Profile.objects.order_by("-elo")[0:1000]
    paginator=Paginator(users,25)
    page_number =request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #extend user model with profile if user signed up via social media
    if request.user.is_authenticated:
        try:
            get_profile = Profile.objects.get(user=request.user)
            
            
        except:
            profile = Profile()
            profile.user= request.user
            profile.nickname = request.user.username
            profile.save()
    return render(request,"main.html",{"users":users,"page_obj":page_obj,"paginator":paginator})
 #no comments just logout   
def logout_user(request):
    logout(request)
    messages.success(request,"You have been  Logged Out...")
    return redirect("main")
def register_user(request):
    #load form and get data from it
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You have been successfully registred")
            
            profile = Profile()
            profile.user= user
            profile.nickname = user.username
            profile.password=password
            profile.save()
            return redirect("main")
            
    else:
        form = SignUpForm()
        return render(request,"register.html",{"form":form})
def login_user(request):
    #getting data from fields and authenticate user
    if request.method == "POST":
        username = request.POST['username']
        password= request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in")
            return redirect('main')
        else:
            messages.success(request,"There was an error ")
            return redirect('main')
    else:
        
        return render(request,"login.html",{})

    
def profile(request,profile_id):
    
    #getting user     
    user = User.objects.get(id=profile_id)
    #filtering tables and get them those were created by user
    tables = Table.objects.filter(created_by=user)
    get_Profile = Profile.objects.get(user=user)
    #make possible queus - so we should make in_queue false everywhere except certain function
    get_Profile.in_queue =False 
    get_Profile.save()
    
    
    followings = Follow.objects.filter(follow_to=user)
    count=0
    try:
        checkfollow= Follow.objects.get(follow_by=request.user,follow_to=user)
        count+=1
    except:
        count-=1
        pass
    
    #creating new table and loading form and gettin a title from it
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save(commit=False)
            table.created_by = request.user
            table.save()
            
            return redirect("table_detail",table_id=table.id)
                
    else:
        form = TableForm()
        
        

    return render(request,"profile.html",{"user":user,"form":form,"tables":tables,"followings":followings,"count_f":count})
    
def table_detail(request,table_id):
    #make possible queus - so we should make in_queue false everywhere except certain function
    if request.user.is_authenticated:
         get_Profile = Profile.objects.get(user=request.user)
         get_Profile.in_queue = False
         get_Profile.save()
    #getting title
    table  = Table.objects.get(id=table_id)
    #getting words from table
    words  = Word.objects.filter(table=table).order_by("-id")
    #in our frontend i check if user equals table.created_by so its not silly and wrong function
    user = table.created_by
    #loading form , getting data from it and creating new word,table.table = table,not commiting cause we need some fill some fields,these fields are nt filling itself so we need to fill it by hand so i dont commit,and we add one to a variable which counts sum of words which were added by concrete user,and we refresh page through redirect function 
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid:
            table = form.save(commit=False)
            table.table = Table.objects.get(id=table_id)
            table.created_by = request.user
            table.save()
            profile = Profile.objects.get(user=user)
            profile.counter =profile.counter+1
            profile.save()
            
            return redirect("table_detail",table_id=table_id)
            
            
            
    else:
        form = WordForm()
        

    return render(request,"table_detail.html",{"words":words,"table":table,"form":form,})

def searchBar(request):
      #make possible queus - so we should make in_queue false everywhere except certain function
     if request.user.is_authenticated:
         get_Profile = Profile.objects.get(user=request.user)
         get_Profile.in_queue =False
         get_Profile.save()
    #checking users name for containing query request
     if request.method == 'GET':
          
          
          query =  request.GET.get('query')
          if query:
               users = User.objects.filter(Q(username__icontains=query))
               counter = users.count()
               return render(request,'searchbar.html',{'users':users,"query":query,"counter":counter})

          else:
               print("No information to show")
               return render(request,"searchbar.html",{})
@login_required
#queue function 
def queue(request):
    from game.models import Game

    #get profile of user who is requesting and changing his queuie status to queue
    get_Profile = Profile.objects.get(user=request.user)
    get_Profile.in_queue =True
    get_Profile.save()
    count = Game.objects.filter(members__in=[request.user]).count()
    
    #if we match second player we are going to a function of creating new game
    if Profile.objects.filter(in_queue =True).count() >=2:

        secondplayer = choice(Profile.objects.filter(in_queue =True))
        if secondplayer != request.user:
            return redirect("game:new_game",secondplayer.id)
    
            
        
    return render(request,"queue.html",{"count":count})
def live_games_counter(request,user_id):
    from game.models import Game
    
    user = User.objects.get(id=user_id)
    count = Game.objects.filter(members__in=[user]).count()
    last_game =Game.objects.filter(members__in=[user]).order_by("-id").first()
    print(last_game)
    return JsonResponse({'live_games_counter':count,"last_game":last_game.id})
        
    
    
    
def tester_words(request):
    if Word.objects.filter(created_by=request.user).count() >0:
        
        random__word =choice(Word.objects.filter(created_by=request.user))
        if request.method =="POST":
            get_test = request.POST.get("form-test")
            if get_test == random__word.word:
                print("good job")
                message = "good job"
            else:
                message = "a bit wrong"
            redirect("random__test")
            return render(request,"test.html",{"word":random__word,"message":message})
    return render(request,"test.html",{"word":random__word})

def about(request):
    if request.method =="POST":
        name = request.POST.get("name__feedback")
        phone = request.POST.get("phone__feedback")
        message = request.POST.get("message__feedback")
        fed  =FeedBack()
        fed.name =name
        fed.phone = phone
        fed.message = message
        fed.save()
    return render(request,"about.html")

#settings view
def settings_profile(request,user):
    user = User.objects.get(username=user)
    return render(request,"profile__settings.html",{"user":user})

def change_ava(request,user_id):
    user = User.objects.get(id=user_id)
    prof =Profile.objects.get(user=user)
    if request.method =="POST":
        new_ava =request.FILES['avatar_photo']
        prof.ava = new_ava
        prof.save()
        return redirect("profile",user.id)
    
def change_nick(request,user_id):
    user = User.objects.get(id=user_id)
    prof =Profile.objects.get(user=user)
    if request.method =="POST":
        new_nick =request.POST.get("nickname")
        prof.nickname = new_nick
        prof.save()
        return redirect("profile",user.id)
def change_password(request,user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    if request.method =="POST":
        old_pass = request.POST.get("old_password")
        new_pass =request.POST.get("new_password")
        
        if old_pass ==profile.password:
            user.set_password(str(new_pass))
            
            user.save()

            profile.password =new_pass
            profile.save()
            user=authenticate(username=user.username,password=new_pass)
            login(request,user)
        
    return redirect("profile",user.id)

def follow(request,user_id):
    follow_obg= Follow()
    follow_to = User.objects.get(id=user_id)
    follow_by = request.user
    follow_obg.follow_by = follow_by
    follow_obg.follow_to = follow_to
    follow_obg.save()
    return redirect("profile",user_id)
def unfollow(request,user_id):
    user = User.objects.get(id=user_id)
    follow = Follow.objects.get(follow_by=request.user,follow_to=user)
    follow.delete()
    return redirect("profile",user_id)

def change_back(request,user_id):
    user = User.objects.get(id=user_id)
    get_prof = Profile.objects.get(user=user)
    if request.method =="POST":
        new_back =request.FILES['background_photo']
        get_prof.background = new_back
        get_prof.save()
        return redirect("profile",user.id)
def delete_back(request,user_id):
    user = User.objects.get(id=user_id)
    get_prof = Profile.objects.get(user=user)
    get_prof.background = get_prof.ava
    get_prof.save()
    return redirect("profile",user.id)

def translator(request):
    return render(request,"translator.html",{})