from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from .models import ToDo
import uuid
from datetime import date

# Create your views here.
def index(request):
	user = request.user
	return render(request, "index.html", {"user": user})

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
	user = request.user
	return render(request, "signup.html", {"user": user})

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
				is_loggedin = True
			except Exception as e:
				raise e

			# messages.success(request, "Logged in successfully")
			return redirect('main:home')

	user = request.user
	return render(request, "login.html", {"user": user})

def home(request):
	user = request.user
	if request.method == "POST":
		if 'new' in request.POST:
			user_object = User.objects.get(username=user)
			todo = request.POST["todo"]
			todo_id = str(uuid.uuid4())
			date_created = date.today()
			ToDo.objects.create(todo_id = todo_id, user=user_object, todo=todo, date_created=date_created)
		elif 'archive' in request.POST:
			todo_id = request.POST["archive"]
			ToDo.objects.filter(todo_id=todo_id).update(is_completed=True)
			return redirect("main:home")
		elif 'delete' in request.POST:
			todo_id = request.POST["delete"]
			ToDo.objects.filter(todo_id=todo_id).delete()
			messages.success(request, "ToDo deleted successfully!")
			return redirect("main:home")
		elif 'unarchive' in request.POST:
			todo_id = request.POST["unarchive"]
			ToDo.objects.filter(todo_id=todo_id).update(is_completed=False)
			return redirect("main:home")

		return redirect('main:home')
	todos = ToDo.objects.filter(user=user, is_completed=False).order_by("-date_created")
	completed_todos = ToDo.objects.filter(user=user, is_completed=True).order_by("-date_created")
	return render(request, "home.html", {"user": user, "todos": todos, "completed_todos": completed_todos} )

def logout(request):
	logout_user(request)
	# user = request.user
	return redirect("main:index")