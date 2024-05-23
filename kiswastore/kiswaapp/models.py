from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class newupdates(models.Model):
    category=models.CharField(max_length=30)
    brand=models.CharField(max_length=30)
    desc=models.TextField()
    price=models.IntegerField()
    img=models.ImageField('upload_to_pics')

    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url

class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(newupdates,on_delete=models.CASCADE)