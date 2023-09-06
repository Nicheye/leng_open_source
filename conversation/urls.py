from django.urls import path

from . import views

app_name = 'conversation'
urlpatterns=[
    path('',views.inbox,name='inbox'),
    path('<int:pk>/',views.detail,name='detail'),
    path('detail_ajax/<int:conversation_id>',views.detail_ajax,name='detail_ajax'),
    path('new/<int:user_id>/',views.new_conversation,name="new"),
]