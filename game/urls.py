from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login"),
    path("signup/", views.signup_page, name="signup"),
    path("game/", views.game_page, name="game"),
    path("play/", views.play_game, name="play"),
    path("history/", views.history_page, name="history"),
    path("logout/", views.logout_user, name="logout"),
]
