from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50)
    count = models.PositiveIntegerField(default=1)


    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    