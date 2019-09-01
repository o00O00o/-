from django.db import models


class State(models.Model):
    liquid_level = models.FloatField(default=13.5)
    temperature = models.IntegerField(default=180)
    low_set = models.IntegerField(default=10)
    high_set = models.IntegerField(default=20)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.time)
