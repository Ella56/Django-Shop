from django.db import models

from accounts.models import Profile
# Create your models here.



# class Stars(models.Model):
    # star = models.


class Color(models.Model):
    color = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)


    def __str__(self):
        return self.color




class Gauarnty(models.Model):
    pass


class Category(models.Model):
    category = models.CharField(max_length=120,unique=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True,blank=True, 
        related_name='subcategories'
        )
    
    image = models.ImageField(upload_to="category",default="default.jpg")


    def __str__(self):
        return (f"{self.parent.name} / {self.name}" if self.parent else {self.name})



    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"



    def dynamic_id(self):
        return self.id - 1


class Specification_Type(models.Model):
    type = models.CharField(max_length=120)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)


    def __str__(self):
        return self.type


class Product(models.Model):
    name = models.CharField(max_length=100)
    img1 = models.ImageField(upload_to="product",default="default.jpg")
    img2 = models.ImageField(upload_to="product",default="default.jpg")
    img3 = models.ImageField(upload_to="product",default="default.jpg")
    img4 = models.ImageField(upload_to="product",default="default.jpg")
    content = models.TextField()
    description = models.TextField()
    review = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ManyToManyField(Color, blank=True)
    price = models.PositiveBigIntegerField()
    quantity = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    



    def get_comments(self):
        return self.comments.filter(status = True)
    
    def comment_count(self):
        return self.comments.count()
    

    def get_specifications(self):
        return self.specifications.all()





class Product_Specifications(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="specifications")
    specification = models.ForeignKey(Specification_Type,on_delete=models.CASCADE)
    value = models.CharField(max_length=200)


    def __str__(self):
        return f"{self.product.name} - {self.specification.type} : {self.value}"








class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(Profile,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.name.user.email

    def get_replies(self):
        return self.replies.filter(status = True)



class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE, related_name='replies')
    name = models.ForeignKey(Profile,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.name.user.email
