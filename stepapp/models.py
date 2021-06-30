from django.db import models
from django.contrib.auth.models import User

class XmlModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"File id:{self.id}"

class Post(models.Model):
    keyword = models.CharField(max_length=255)
    min_videos = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)

class Csv(models.Model):
    field = models.CharField(max_length=255, null=True)
    file_name = models.FileField(upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    def __str__(self):
        return f"File id: {self.id}"


# do3ensKE
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    productName=models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    image=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    creted_on=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"File id:{self.id}"
class ProductSearch(models.Model):
    userInfo = models.CharField(max_length=255, blank=True, null=True)
    searchTerm = models.CharField(max_length=255)
    min_search = models.IntegerField()
    creted_on=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"File id:{self.id}"

class IdSearch(models.Model):
    userInfo = models.CharField(max_length=255)
    ids = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"File id:{self.id}"

