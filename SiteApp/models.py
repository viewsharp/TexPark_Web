from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=64, null=False)
    avatar = models.ImageField(upload_to='media/images/user-avatar', null=False)


class LikeAbleModel(models.Model):
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    def like(self, user):
        self.dislikes.remove(user)
        self.likes.add(user)

    def dislike(self, user):
        self.likes.remove(user)
        self.dislikes.add(user)

    # class Meta:
        # abstract = True


class Tag(models.Model):
    title = models.CharField(max_length=32, null=False)


class Quest(LikeAbleModel):
    title = models.CharField(max_length=96, null=False)
    text = models.TextField(max_length=960, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    date = models.DateField(auto_now=True)
    correct_answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, default=None)

    class Meta:
        abstract = True


class Answer(LikeAbleModel):
    text = models.TextField(max_length=960)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='author')
    question = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='quest')
    date = models.DateField(auto_now=True)
