from django.db import models

class TestData(models.Model):
    json_text = models.TextField()
    csv_text = models.TextField()

