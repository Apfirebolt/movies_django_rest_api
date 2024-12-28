from django.db import models


class Movie(models.Model):
    ID = models.IntegerField(primary_key=True, auto_created=True)
    Movie_Name = models.CharField(max_length=100)
    Year = models.IntegerField()
    Timing = models.CharField(max_length=50)
    Rating = models.FloatField(null=True, blank=True)
    Votes = models.CharField(max_length=50)
    Genre = models.CharField(max_length=100)
    Language = models.CharField(max_length=100)

    def __str__(self):
        return self.Movie_Name
    
    class Meta:
        db_table = 'movies_table'


class Game(models.Model):
    img = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=100)
    console = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    publisher = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    critic_score = models.FloatField(null=True, blank=True)
    total_sales = models.FloatField(null=True, blank=True)
    na_sales = models.FloatField(null=True, blank=True)
    jp_sales = models.FloatField(null=True, blank=True)
    pal_sales = models.FloatField(null=True, blank=True)
    other_sales = models.FloatField(null=True, blank=True)
    release_date = models.CharField(max_length=50,null=True, blank=True)
    last_update = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'games_table'

    def __str__(self):
        return self.title
