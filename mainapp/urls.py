from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.main,name="main"),
    
    path("login/",views.login_user,name="login"),
    path("profile/<int:profile_id>",views.profile,name="profile"),
    path("table/<int:table_id>",views.table_detail,name="table_detail"),
    path("logout/",views.logout_user,name="logout"),
    path("register/",views.register_user,name="register"),
    path('search/',views.searchBar,name="search"),
    path("queue",views.queue,name="queue"),
    path("test",views.tester_words,name="random__test"),
    path("about",views.about,name="about"),
    path("settings/<slug:user>",views.settings_profile,name="setting_profile"),
    path("change_ava/<int:user_id>",views.change_ava,name="change_ava"),
    path("change_nick/<int:user_id>",views.change_nick,name="change_nick"),
    path("change_password/<int:user_id>",views.change_password,name="change_password"),
    path("follow/<int:user_id>",views.follow,name="follow"),
    path("unfollow/<int:user_id>",views.unfollow,name="unfollow"),
    path("changeback/<int:user_id>",views.change_back,name="change_background"),
    path("deleteback/<int:user_id>",views.delete_back,name="delete_background"),
    
    path("live_games_counter/<int:user_id>",views.live_games_counter,name="live_games_counter")
]

