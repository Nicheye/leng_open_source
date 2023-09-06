from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . models import table,word,Profile

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	


	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class TableForm(forms.ModelForm):
	class Meta:
		model = table
		fields=("name",)
		widgets= {
			'name':forms.TextInput(attrs={
				"type":"text",
				"class":"form-control",
				"name:":"table_form",
				"placeholder":"Title",
				"required":"true",
				
			})
		}
class WordForm(forms.ModelForm):
	class Meta:
		model = word
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

