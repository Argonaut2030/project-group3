from django.db import models

# Create your models here.
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False, unique=True)

    def __str__(self):
        return self.name
