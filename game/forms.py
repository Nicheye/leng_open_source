from django import forms
from .models import word_game
#from .models import GameMessage
#class GameMessageForm(forms.ModelForm):
#    class Meta:
#        model = GameMessage
#        fields = ('content',)
#        widgets={
#            'content':forms.Textarea(attrs={
#            'class':'form-control'
#            })
#        }

class WordForm(forms.ModelForm):
	class Meta:
		model = word_game
		fields=("word","wordineng")
		widgets= {
			'word':forms.TextInput(attrs={
				"type":"text",
				"class":"form-control",
				"name:":"word_form",
				"placeholder":"word",
				"required":"true",
				
			}),
			'wordineng':forms.TextInput(attrs={
				"type":"text",
				"class":"form-control",
				"name:":"wordineng_form",
				"placeholder":"word in eng",
				"required":"true",
				
			})
		}
