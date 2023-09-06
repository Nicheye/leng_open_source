from django.db import models
from mainapp.models import table
from django.contrib.auth.models import User

from django.utils import timezone
# Create your models here.
class Game(models.Model):
    
    members = models.ManyToManyField(User,related_name='game_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-modified_at',)

class Round(models.Model):
    round_number = models.IntegerField()
    game =  models.ForeignKey(Game,related_name='game_round',on_delete=models.CASCADE,default=None,)
    writer_player = models.ForeignKey(User,related_name='writer_player',on_delete=models.CASCADE)
    guesser_player = models.ForeignKey(User,related_name='guesser_player',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    current_player = models.ForeignKey(User,related_name='current_player',on_delete=models.CASCADE)
    waiter_player = models.ForeignKey(User,related_name='waiter_player',on_delete=models.CASCADE)
#class GameMessage(models.Model):
#    conversation = models.ForeignKey(Game,related_name='game_messages',on_delete=models.CASCADE)
#    content = models.TextField()
#    created_at = models.DateTimeField(auto_now_add=True)
#    created_by = models.ForeignKey(User,related_name='game_created_messages',on_delete=models.CASCADE)
#class table_game(models.Model):
#    conversation = models.ForeignKey(Game,related_name='game_messages',on_delete=models.CASCADE)
#    created_by = models.ForeignKey(User,related_name='created_tables',on_delete=models.CASCADE)
#    name = models.CharField(max_length=50)
#    created_at = models.DateTimeField(auto_now_add=True)
#    def __str__(self):
#        return self.name   
class word_game(models.Model):
    conversation = models.ForeignKey(Game,related_name='game_messages',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name='created_words_game',on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    wordineng=models.CharField(max_length=100)
    solved = models.BooleanField(default=False)
    round = models.ForeignKey(Round,related_name="round_word_game",on_delete=models.CASCADE)
    def __str__(self):
        return self.word

class Score(models.Model):
    game =  models.ForeignKey(Game,related_name='game',on_delete=models.CASCADE)
    user  = models.ForeignKey(User,related_name='player',on_delete=models.CASCADE)
    score = models.IntegerField(default=0)