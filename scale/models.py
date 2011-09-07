from django.db import models

class Dataset(models.Model):
    name = models.TextField()

class Row(models.Model):
    dataset = models.ForeignKey(Dataset)
    csv_text = models.TextField()
