from django.db import models
# Create your models here.

class Review (models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    content = models.TextField(null=False)
    movie = models.CharField(max_length=20)
    
class Comment (models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    user =  models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField(null=False)