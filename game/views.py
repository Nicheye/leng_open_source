from django.shortcuts import render,get_object_or_404,redirect
from mainapp.models import table
from .models import Game,Round,word_game
from django.contrib.auth.decorators import login_required
from .forms import WordForm
#from .forms import GameMessageForm
import random


from django.http import JsonResponse,HttpResponse
import datetime
from django.utils import timezone
from .models import Score
from django.contrib.auth.models import  User
from mainapp .models import Profile,table as Table
# Create your views here.
@login_required
def new_conversation_game(request,user_pk):
    #gettint user and checking for same user and already game which is not finished and if game exists to redirect to the game
    user = get_object_or_404(User,id=user_pk)

    if user == request.user:
        return redirect("profile",request.user.id)
    conversations = Game.objects.filter(members__in=[request.user.id],is_finished=False)
     
#     if conversations:
#         return redirect("game:detail_game",pk=conversations.first().id)
    
            #if doesnt find existing game
            #creates new game and adds two member  - requester and requested
    conversation = Game.objects.create()
    conversation.members.add(request.user)
    conversation.members.add(user)
    conversation.save()
            #starts round and sets player`s roles
    round = Round()
    round.round_number=i
    round.game = conversation
    round.date = timezone.now()
    round.writer_player= conversation.members.first()
    for member in conversation.members.filter():
       if round.writer_player !=member:
            round.guesser_player = member
    round.current_player = round.writer_player
    round.waiter_player = round.guesser_player
    round.save()
            
            #and sets a scores for each player
    score_writter = Score()
    score_writter.game = conversation
    score_writter.user = round.writer_player
    score_writter.score = 0
    score_writter.save()
    score_gusser = Score()
    score_gusser.game = conversation
    score_gusser.user = round.guesser_player
    score_gusser.score = 0
    score_gusser.save()
            
            #return redirect('game:detail_game',pk=item_pk)
    get_last_game = Game.objects.filter(members__in=[request.user.id]).order_by("-id").first()
    
    return redirect("game:detail_game",get_last_game.id)
    
@login_required
#checks for existed and existing game and filters them by is_finished status
def inbox_game(request):
     conversations = Game.objects.filter(members__in=[request.user.id],is_finished=False)
     conversations_past = Game.objects.filter(members__in=[request.user.id],is_finished=True)
     from mainapp .models import Profile
     get_Profile = Profile.objects.get(user=request.user)
     get_Profile.in_queue = False
     get_Profile.save()
     return render(request,'inbox_game.html',{
          'conversations':conversations,
          'conversations_past':conversations_past
     })


i=1



@login_required
def detail_game(request,pk):
     #gets game
     conversation = Game.objects.filter(members__in=[request.user.id]).get(pk=pk)
     
     #gets round
     round_get = Round.objects.filter(game=conversation).order_by("-id").first()
     #messages = conversation.game_messages.filter(round=round_get)
     #gets roles and score data
     writer =round_get.writer_player
     guesser = round_get.guesser_player
     
     get_score = Score.objects.filter(game=conversation)
     Profile_writer = Profile.objects.get(user=writer)
     Profile_guesser= Profile.objects.get(user=guesser)
     get_score1 = get_score.get(user=writer)
     get_score2 = get_score.get(user=guesser)
     
     #function of finishing game,cheks for variable of number and status of is_finished
     if round_get.round_number >=10 and conversation.is_finished==False:
           
           #if get_score is equal we keep playing in other way
           if get_score1.score == get_score2.score:
               pass
           else:
                 #plusing and minusing elo
                 
                 if get_score1.score>get_score2.score:
                       #writer.
                       
                       Profile_writer.elo = Profile_writer.elo+25
                       Profile_writer.save()
                       Profile_guesser.elo = Profile_guesser.elo-25
                       Profile_guesser.save()
                       #Table.objects.filter(created_by=writer).order_by("-id").first()
                       
                       
                 if get_score1.score<get_score2.score:
                       #writer.
                       Profile_guesser.elo = Profile_guesser.elo+25
                       Profile_guesser.save()
                       Profile_writer.elo = Profile_writer.elo-25
                       Profile_writer.save()
                 conversation.is_finished =True
                 conversation.save()
     if round_get.date +datetime.timedelta(seconds=30)>timezone.now():
          if request.method =='POST':
               #getting data and swapping roles
               if request.user == writer:
               
                    form = WordForm(request.POST)
                    if form.is_valid():
                         conversation_message = form.save(commit=False)
                         conversation_message.conversation = conversation
                         conversation_message.created_by = request.user
                         conversation_message.round = round_get
                         conversation_message.save()
                         
                         conversation.save()
                         username = form.cleaned_data['word']
                         password = form.cleaned_data['wordineng']
                    #function switches round but i replaced it in html  
                    return redirect('game:detail_game',pk=pk)
          else:
               if request.user == writer:
                    form = WordForm()
     else:     
          new_round(conversation,round_get)
          return redirect('game:detail_game',pk=pk)        

          if request.user ==guesser:
                pass
               #if round_get.date +datetime.timedelta(seconds=30)<timezone.now():
               #         
               #          new_round = Round()
               #          new_round.date = timezone.now()
               #          new_round.game = conversation
               #          
               #          
               #          
               #          new_round.round_number = round_get.round_number+1
               #          if (round_get.round_number+1) %2 !=0:
               #                    new_round.guesser_player = round_get.writer_player
               #                    new_round.writer_player = round_get.guesser_player
               #          
               #          else:
               #                new_round.guesser_player = round_get.guesser_player
               #                new_round.writer_player = round_get.writer_player
               # 
               #          new_round.waiter_player = round_get.current_player
               #          new_round.current_player = round_get.waiter_player
               #          new_round.save()
               #          return redirect("game:detail_game" , conversation.id)


               
               
                  
     
          
     if request.user ==writer:
           return render(request,'detail_converse_game.html',{
          'conversation':conversation,
          'form':form,
          'writer':writer,
           "guesser":guesser,
          'round':round_get,
          'score':get_score,
          'score_1':get_score1.score,
          'score_2':get_score2.score,
          
          #'messages':messages
           })
     else:
           return render(request,'detail_converse_game.html',{
          'conversation':conversation,
          'writer':writer,
          "guesser":guesser,
          'round':round_get,
          'score':get_score,
          'score_1':get_score1.score,
          'score_2':get_score2.score,
         
          #'messages':messages
          
          
     })
def new_round(conversation,round_get):
     new_round = Round()
     new_round.date = timezone.now()
     new_round.game = conversation                    
     new_round.round_number = round_get.round_number+1
     if (round_get.round_number) %2 !=0:
                                   
          new_round.guesser_player = round_get.writer_player
          new_round.writer_player = round_get.guesser_player
                         
     else:
                               
          new_round.guesser_player = round_get.guesser_player
          new_round.writer_player = round_get.writer_player

     new_round.waiter_player = round_get.current_player
     new_round.current_player = round_get.waiter_player
     new_round.save()
#small in_game api for test(if we can call it api xD)
def tester(request,message_id,game_id):
     game  =Game.objects.get(id=game_id)
     get_score=Score.objects.filter(game=game)
     
     game_message = word_game.objects.get(id=message_id)
     round_get = game_message.round
     current_round_get = Round.objects.filter(game=game).order_by("-id").first()
     
     if request.method =='POST':
          get_guess = request.POST.get("form-guess")
          if game_message.word == get_guess:
               change_score = get_score.get(user=request.user)
               change_score.score = change_score.score+1
               change_score.save()
               game_message.solved =True
               game_message.save()
          #function switches round but i replaced it in html
          if current_round_get.date +datetime.timedelta(seconds=30)<timezone.now():
                         new_round(game,round_get)
          # #              
          return redirect("game:detail_game" , game_id)
#skip functio get data and equal one to a value of rounds and swap the roles                        
def skip(request,game_id,round_id):         
     get_game = Game.objects.get(id=game_id)
     round_get  = Round.objects.filter(game=get_game).get(id=round_id)
     new_round(get_game,round_get)
     
     return redirect("game:detail_game" , game_id)
#for ajax and refreshing
def get_count_messages(request,conversation_id):
      get_conver = Game.objects.get(id=conversation_id)
      count = get_conver.game_messages.count()
      round_geget_count_messagest = Round.objects.filter(game=get_conver).order_by("-id").first()
      round_get = round_geget_count_messagest.round_number
      return JsonResponse({"current_num":count,"round_num_get":round_get})