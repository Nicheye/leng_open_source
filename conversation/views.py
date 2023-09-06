from django.shortcuts import render,get_object_or_404,redirect
from mainapp.models import table
from .models import Conversation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ConversationMessageForm
from django.http import JsonResponse
from django.core import serializers
# Create your views here.
@login_required
def new_conversation(request,user_id):
    #get user and check for same user and add users and send message which we get from loaded form and we dont commit cause we fill foreign keys fields in db
    user = get_object_or_404(User,id=user_id)

    if user == request.user:
        return redirect("profile",request.user.id)
#     conversations = Conversation.objects.filter(members__in=[request.user,user])

#     if conversations:
#         return redirect("conversation:detail",pk=conversations.first().id)
    
    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create()
            conversation.members.add(request.user)
            conversation.members.add(user)
            conversation.save()
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            last_chat =Conversation.objects.filter(members__in=[request.user.id]).order_by("-id").first()
            return redirect('conversation:detail',last_chat.id)
    else:
            form = ConversationMessageForm()
           
    return render(request,'new.html',{
         'form':form
    })
@login_required
#list of convs
def inbox(request):
     from mainapp .models import Profile
     get_Profile = Profile.objects.get(user=request.user)
     get_Profile.in_queue = False
     get_Profile.save()
     conversations = Conversation.objects.filter(members__in=[request.user.id])
     
     return render(request,'inbox.html',{
          'conversations':conversations
     })

@login_required
#getting messages and send message which we get from forms which was loaded
def detail(request,pk):
     conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
     
         
     
     if request.method =='POST':
          form = ConversationMessageForm(request.POST)
          if form.is_valid():
               conversation_message = form.save(commit=False)
               conversation_message.conversation = conversation
               conversation_message.created_by = request.user
               conversation_message.save()

               conversation.save()
               
               return redirect('conversation:detail',pk=pk)
     else:
               
               form = ConversationMessageForm()
     

     return render(request,'detail_converse.html',{
          'conversation':conversation,
          'form':form
     })
def detail_ajax(request,conversation_id):
     conversation = Conversation.objects.get(id=conversation_id)
     conv = conversation.messages.all()
     conv_seri = serializers.serialize("json",conv)
     return JsonResponse(conv_seri,safe=False)

