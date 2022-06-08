from django.contrib.auth.models import User
from django.db import models


class AddTags(models.Model):
    tags = models.CharField(max_length=100)

    def __str__(self):
        return self.tags


class Post(models.Model):
    title = models.CharField(max_length=250)
    post_tags = models.ForeignKey(AddTags, on_delete=models.CASCADE)
    full_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upload = models.ImageField(upload_to='uploads/', null=True)

    def __str__(self):
        return self.title

    def get_total_likes(self):
        return self.like_set.count()


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
