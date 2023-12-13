from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description =models.TextField()

    class Meta:
        verbose_name = 'notes'
        verbose_name_plural ='notes'

    def __str__(self) -> str:
        return self.title
