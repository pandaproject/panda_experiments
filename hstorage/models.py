from django.db import models
from django_hstore import hstore

class Dataset(models.Model):
    name = models.TextField()

class Row(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='rows')
    csv_text = models.TextField()
    columns = hstore.DictionaryField()

    objects = hstore.Manager()

