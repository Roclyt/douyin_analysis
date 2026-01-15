from django.db import models

# Create your models here.

class VideoData(models.Model):
    """
    视频信息表
    """
    userName = models.TextField(verbose_name='用户名', null=True, blank=True)
    fansCount = models.BigIntegerField(verbose_name='粉丝数', null=True, blank=True)
    description = models.TextField(verbose_name='视频描述', null=True, blank=True)
    awemeId = models.TextField(verbose_name='视频ID', null=True, blank=True)
    publishTime = models.DateTimeField(verbose_name='发布时间', null=True, blank=True)
    duration = models.TextField(verbose_name='视频时长', null=True, blank=True)
    commentCount = models.TextField(verbose_name='评论数', null=True, blank=True)
    likeCount = models.BigIntegerField(verbose_name='点赞数', null=True, blank=True)
    shareCount = models.BigIntegerField(verbose_name='分享数', null=True, blank=True)
    collectCount = models.BigIntegerField(verbose_name='收藏数', null=True, blank=True)


    class Meta:
        verbose_name = '视频信息'
        db_table = 'video_data'

class CommentData(models.Model):
    """
    评论信息表
    """
    userId = models.BigIntegerField(verbose_name='用户ID', null=True, blank=True)
    userName = models.TextField(verbose_name='用户名', null=True, blank=True)
    commentTime = models.DateTimeField(verbose_name='评论时间', null=True, blank=True)
    userIP = models.TextField(verbose_name='用户IP', null=True, blank=True)
    content = models.TextField(verbose_name='评论内容', null=True, blank=True)
    likeCount = models.BigIntegerField(verbose_name='点赞数', null=True, blank=True)
    awemeId = models.BigIntegerField(verbose_name='视频ID', null=True, blank=True)

    class Meta:
        verbose_name = '评论信息'
        db_table = 'comment_data'