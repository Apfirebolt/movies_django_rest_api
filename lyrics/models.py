from django.db import models

# Create your models here.
class Lyrics(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    film = models.CharField(max_length=100, null=True, blank=True)
    singer = models.CharField(max_length=100, null=True, blank=True)
    composer = models.CharField(max_length=100, null=True, blank=True)
    lyricist = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    lyrics = models.TextField()

    def __str__(self):
        return self.title + " - " + self.singer + " - " + str(self.year)