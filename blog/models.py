from django.db import models
from django_movie_api.settings import AUTH_USER_MODEL


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'blog_table'


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'blog_post_table'


class PostImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images')
    caption = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images/post')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.post.title + '-' + self.caption
    
    class Meta:
        db_table = 'post_image_table'


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    caption = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images/blog')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.blog.title + '-' + self.caption
    
    class Meta:
        db_table = 'blog_image_table'

    

    


