from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from .models import ToDo
import uuid
# Create your views here.
def index(request):
	return render(request, "index.html")

def signup(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]
		password = request.POST["password"]
		confirm_password = request.POST["confirm_password"]

		if password!=confirm_password:
			messages.error(request, "Password and Confirm Password should be same")
			return redirect('main:signup')

		username_already_exists = list(User.objects.filter(username=username))

		if len(username_already_exists)!=0:
			messages.info(request, "User with username {} already exists".format(username))
			return redirect('main:signup')

		email_already_exists = list(User.objects.filter(email=email))

		if len(email_already_exists)!=0:
			messages.info(request, "User with email {} already exists".format(email))
			return redirect('main:signup')

		try:
			User.objects.create_user(username=username, email=email, password=password)
			messages.success(request, "username {} registered successfully".format(username))
			return redirect("main:login")
		except Exception as e:
			raise e

	return render(request, "signup.html")

def login(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]

		try:
			user = authenticate(username=username, password=password)
		except Exception as e:
			raise e

		if user is not None:
			try:
				login_user(request, user)
			except Exception as e:
				raise e

			# messages.success(request, "Logged in successfully")
			return redirect('main:home')

	return render(request, "login.html")

def home(request):
	user = request.user
	if request.method == "POST":
		user_object = User.objects.get(username=user)
		todo = request.POST["todo"]
		todo_id = str(uuid.uuid4())
		ToDo.objects.create(todo_id = todo_id, user=user_object, todo=todo)
		return redirect('main:home')
	return render(request, "home.html", {"user": user})