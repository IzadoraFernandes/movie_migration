from django.db import models

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie, related_name='genres')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MovieTag(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    relevance = models.FloatField()

    class Meta:
        unique_together = ('movie', 'tag')


class Rating(models.Model):
    user_id = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ('user_id', 'movie')

    def __str__(self):
        return f'{self.movie.title} - {self.rating}'


class Link(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=10, null=True, blank=True)
    tmdb_id = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.movie.title} - IMDb: {self.imdb_id}, TMDb: {self.tmdb_id}'
