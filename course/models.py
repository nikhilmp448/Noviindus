from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100, null=True)
    subtitle = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="image/course")
    description = models.TextField(max_length=1000)
    amountintext = models.CharField(max_length=100)
    amountinvalue = models.FloatField()
    status = models.BooleanField()

    def __str__(self):
        return self.title