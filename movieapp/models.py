from django.db import models

# Create your models here.
class Movie(models.Model):
    mname=models.CharField(max_length=50)
    class Meta:
        db_table = "movie"
class Moviereview(models.Model):
    review=models.CharField(max_length=100)
    sentinaive=models.CharField(max_length=100)
    sentivader=models.CharField(max_length=100)
    movieid=models.IntegerField()
    class Meta:
        db_table = "moviereview"

