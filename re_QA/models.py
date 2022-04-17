from django.db import models
from django.utils import timezone

# Create your models here.
class Topic(models.Model):

    comment     = models.CharField(verbose_name="コメント",max_length=2000)
    dt      = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    
    def __str__(self):
        return self.comment