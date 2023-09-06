from django.contrib import admin
from .models import Game,Round,Score,word_game
#from .models import GameMessage
# Register your models here.
admin.site.register(Game)
#admin.site.register(GameMessage)
admin.site.register(Round)
admin.site.register(word_game)
admin.site.register(Score)