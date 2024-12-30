from django.db import models
from django_movie_api.settings import AUTH_USER_MODEL
from django.utils.text import slugify


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tags", related_name="blogs", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blog_table"


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField()
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="posts", null=True, blank=True
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True,
    )
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tags", related_name="blog_posts", blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    class Meta:
        db_table = "blog_post_table"


class PostImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="images")
    caption = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="images/post")
    order = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tags", related_name="post_images", blank=True)

    def __str__(self):
        return self.post.title + "-" + self.caption

    class Meta:
        db_table = "post_image_table"


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="images")
    caption = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="images/blog")
    order = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tags", related_name="blog_images", blank=True)

    def __str__(self):
        return self.blog.title + "-" + self.caption

    class Meta:
        db_table = "blog_image_table"


class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
    )
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    technology = models.CharField(max_length=250, null=True, blank=True)
    project_link = models.URLField(null=True, blank=True)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tags", related_name="projects", blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        db_table = "project_table"


class ProjectImages(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    caption = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="images/project")
    order = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tags", related_name="project_images", blank=True)

    def __str__(self):
        return self.project.title + "-" + self.caption

    class Meta:
        db_table = "project_image_table"


class GalleryPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gallery_posts",
        null=True,
        blank=True,
    )
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tags", related_name="gallery_posts", blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(GalleryPost, self).save(*args, **kwargs)

    class Meta:
        db_table = "gallery_post_table"


class GalleryPostImages(models.Model):

    post = models.ForeignKey(
        GalleryPost, on_delete=models.CASCADE, related_name="images"
    )
    caption = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="images/gallery_post")
    order = models.IntegerField(default=0)
    tags = models.ManyToManyField(
        "Tags", related_name="gallery_post_images", blank=True
    )

    def __str__(self):
        return self.post.title + "-" + self.caption

    class Meta:
        db_table = "gallery_post_image_table"


class Tags(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tags_table"


class GenericImage(models.Model):
    caption = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="images/generic")

    def __str__(self):
        return self.caption

    class Meta:
        db_table = "generic_image_table"
