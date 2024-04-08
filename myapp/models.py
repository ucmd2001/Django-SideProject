from django.db import models

class Event(models.Model):
    uid = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)

class ShowInfo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    time = models.DateTimeField()
    location = models.CharField(max_length=255)

class MasterUnit(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    master_unit_name = models.CharField(max_length=100)
