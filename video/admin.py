from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import VideoData, CommentData


@admin.register(VideoData)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['awemeId', 'userName', 'description', 'likeCount', 'commentCount', 'publishTime']
    list_filter = ['publishTime']
    search_fields = ['awemeId', 'userName', 'description']
    ordering = ['-publishTime']
    list_per_page = 50
    date_hierarchy = 'publishTime'

    def description_preview(self, obj):
        """预览描述"""
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description
    description_preview.short_description = '描述'

    def like_count_display(self, obj):
        """格式化显示点赞数"""
        if obj.like_count >= 10000:
            return f"{obj.like_count / 10000:.1f}w"
        return str(obj.like_count)
    like_count_display.short_description = '点赞数'


@admin.register(CommentData)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['userId', 'userName', 'content_preview', 'likeCount', 'commentTime', 'awemeId']
    list_filter = ['commentTime', 'userIP']
    search_fields = ['userName', 'content', 'awemeId']
    ordering = ['-commentTime']
    list_per_page = 50
    date_hierarchy = 'commentTime'

    def content_preview(self, obj):
        """预览评论内容"""
        if len(obj.content) > 30:
            return obj.content[:30] + '...'
        return obj.content
    content_preview.short_description = '评论内容'


# Admin site配置
admin.site.site_header = '抖音数据分析系统'
admin.site.site_title = '抖音数据分析系统'
admin.site.index_title = '欢迎使用抖音数据分析系统'
