from django.db import models
from accounts.models import Profile
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class Color(models.Model):
    color = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)


    def __str__(self):
        return self.color



class Category(models.Model):
    name = models.CharField(max_length=120,unique=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True,blank=True, 
        related_name='subcategories'
        )
    
    image = models.ImageField(upload_to="category",default="default.jpg")


    def __str__(self):
        return (f"{self.parent.name} / {self.name}" if self.parent else self.name)



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
    discount_price = models.PositiveBigIntegerField(default=0)
    guaranty = models.ManyToManyField("Guaranty", blank=True )
    total_sold = models.PositiveIntegerField(default=0)
    total_views = models.PositiveBigIntegerField(default=0)
    total_favorites = models.PositiveBigIntegerField(default=0)
    total_vots = models.PositiveIntegerField(default=0)
    has_discount = models.BooleanField(default=False)
    has_guaranty = models.BooleanField(default=False)
    has_color = models.BooleanField(default=True)
    availability = models.BooleanField(default=True)
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
    
    def get_average_score(self):
        scores = self.scores.all()
        if scores.exists():
            total_score = sum([item.score for item in scores])
            return round(total_score / scores.count())
        return 0
    

    def get_discounted_price(self):
        price = int(self.price) - (int(self.price) * int(self.discount_price) / 100 )
        price = round(price)
        return str(price)





class Product_Specifications(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="specifications")
    specification = models.ForeignKey(Specification_Type,on_delete=models.CASCADE)
    value = models.CharField(max_length=200)


    def __str__(self):
        return f"{self.product.name} - {self.specification.type} : {self.value}"



class ProductScore(models.Model):
    product = models.ForeignKey(Product, related_name='scores', on_delete=models.CASCADE)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.user.email


class Guaranty(models.Model):
    months = models.PositiveBigIntegerField(default=0)
    price_increase = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.months)



class SpecialOffer(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    


    def remaining_time(self):
        remaining = self.end_date - timezone.now()


        if remaining.total_seconds() < 0 :
            return {"days":0, "hours":0, "minutes":0, "seconds":0}
        
        # days = remaining.days
        # hours, remainder = divmod(remaining.seconds, 3600)
        # minutes, seconds = divmod(remainder, 60)
        total_seconds = int(remaining.total_seconds())
        days, remainder = divmod(total_seconds, 86400)  # 86400 seconds in a day
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return {"days": days, "hours":hours, "minutes":minutes, "seconds":seconds,}
    
    def __str__(self):
        return self.product.name

class Compare(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name.user.email
    
    class Meta:
        ordering = ["-created_at"]


class Favorites(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.user.email




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
