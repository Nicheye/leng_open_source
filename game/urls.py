from django.urls import path

from . import views
app_name = 'game'
urlpatterns=[
    path('',views.inbox_game,name='inbox_game'),
    path('<int:pk>/',views.detail_game,name='detail_game'),
    path('get_count_images/<int:conversation_id>',views.get_count_messages,name='get_count_msg'),
   
    path('new/<int:user_pk>/',views.new_conversation_game,name="new_game"),
    path('<int:game_id>/<int:message_id>/',views.tester,name="tester"),
    path('skip/<int:game_id>/<int:round_id>',views.skip,name="skip"),
    
]