from django.db import models

class User(models.Model):
    mobile = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.mobile


class GameHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.CharField(max_length=5)
    result = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game_id} - {self.result}"
