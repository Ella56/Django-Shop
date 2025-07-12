from django.db import models

# Create your models here.



# class Stars(models.Model):
    # star = models.


class Specification_Type(models.Model):
    pass



class Specifications(models.Model):
    pass

class Color(models.Model):
    pass



class Gauarnty(models.Model):
    pass


class Product_Category(models.Model):
    pass







class Product(models.Model):
    name = models.CharField(max_length=100)
    img1 = models.ImageField(upload_to="product",default="default.jpg")
    img2 = models.ImageField(upload_to="product",default="default.jpg")
    img3 = models.ImageField(upload_to="product",default="default.jpg")
    img4 = models.ImageField(upload_to="product",default="default.jpg")
    content = models.TextField()



