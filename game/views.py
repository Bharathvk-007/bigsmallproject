import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User, GameHistory

# LOGIN PAGE
def login_page(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        user = User.objects.filter(mobile=mobile, password=password).first()
        if user:
            request.session["user_id"] = user.id
            return redirect("game")
        else:
            return render(request, "login.html", {
                "error": "Invalid mobile number or password"
            })

    return render(request, "login.html")


# SIGNUP PAGE
def signup_page(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        if User.objects.filter(mobile=mobile).exists():
            return render(request, "signup.html", {
                "error": "Mobile number already registered"
            })

        User.objects.create(mobile=mobile, password=password)

        # After signup → go to login page
        return redirect("login")

    return render(request, "signup.html")


# GAME PAGE
def game_page(request):
    if "user_id" not in request.session:
        return redirect("login")
    return render(request, "game.html")


# PLAY GAME (SHOW RESULT + SAVE HISTORY)
def play_game(request):
    if "user_id" not in request.session:
        return JsonResponse({"error": "Not logged in"}, status=401)

    game_id = request.POST.get("id")

    if not game_id or not game_id.isdigit() or len(game_id) != 5:
        return JsonResponse({"error": "Enter valid 5-digit ID"})

    random.seed(game_id)
    result = random.choice(["Big", "Small"])

    user = User.objects.get(id=request.session["user_id"])

    GameHistory.objects.create(
        user=user,
        game_id=game_id,
        result=result
    )

    return JsonResponse({
        "game_id": game_id,
        "result": result
    })


# HISTORY PAGE
def history_page(request):
    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(id=request.session["user_id"])
    history = GameHistory.objects.filter(user=user).order_by("-created_at")

    return render(request, "history.html", {"history": history})


# LOGOUT
def logout_user(request):
    request.session.flush()
    return redirect("login")
