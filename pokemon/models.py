from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    pokemon_id = models.PositiveIntegerField(unique=True)
    abilities = models.JSONField()
    types = models.JSONField()
    stats = models.JSONField()

    def __str__(self):
        return self.name


class SearchHistory(models.Model):
    query = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.query} - {self.timestamp}"
