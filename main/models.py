from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Summarized(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	text = models.CharField(max_length = 50)
	text_input = models.TextField()
	text_output = models.TextField()
	created_date = models.DateTimeField(blank = True, null = True)

	def create(self):
		self.created_date = timezone.now()
		self.save()

	def __str__(self):
		return self.text
