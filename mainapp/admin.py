from django.contrib import admin
from . models import word,table,Profile,FeedBack,Follow
# Register your models here.
admin.site.register(word)
admin.site.register(table)
admin.site.register(Profile)
admin.site.register(FeedBack)
admin.site.register(Follow)