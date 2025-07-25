from django.db import models
from accounts.models import Profile

# Create your models here.



class Category(models.Model):
    category = models.CharField(max_length=150)
    status = models.BooleanField(default=True)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="blog",default="default.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True,blank=True)
    status = models.BooleanField(default=False)
    total_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def truncate_chars(self):
        return self.content[:100]
    
    def get_comments(self):
        return self.comments.filter(status = True)
    

    def comment_count(self):
        return self.comments.count()




class Blog_Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE, related_name='comments')
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



class Blog_Reply(models.Model):
    comment = models.ForeignKey(Blog_Comment,on_delete=models.CASCADE, related_name='replies')
    name = models.ForeignKey(Profile,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.name.user.email
