from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ToDo(models.Model):
	todo_id = models.CharField(max_length=255, primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	todo = models.TextField()
	is_completed = models.BooleanField(default=False)
	# due_date = models.DateField()
	date_created = models.DateField()