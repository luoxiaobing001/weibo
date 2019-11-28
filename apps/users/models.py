from django.db import models
from django.contrib.auth.models import  User


class Attention(models.Model):
    follow = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follow",verbose_name="关注者")
    followed = models.ForeignKey(User,on_delete=models.CASCADE, related_name='followed',verbose_name="被关注者")

    class Meta:
        db_table = 'tb_attention'
        verbose_name = "关注表"
        verbose_name_plural = verbose_name

class Blog(models.Model):
    release = models.ForeignKey(User,on_delete=models.CASCADE,related_name="release",verbose_name="发布者")
    content = models.TextField(verbose_name="微博内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'tb_blog'
        verbose_name = "微博"
        verbose_name_plural = verbose_name