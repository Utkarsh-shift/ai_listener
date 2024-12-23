from django.db import models
class interviewTest(models.Model):
    file = models.FileField(upload_to="")

class interviewTest1(models.Model):
    file = models.FileField()
# Create your models here.
