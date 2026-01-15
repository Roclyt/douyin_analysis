#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/15 9:12
# @Author  : Rocky


"""
URL配置
"""

from django.urls import path
from . import views

app_name = 'video'

urlpatterns = [
    # 页面路由
    path('', views.index, name='index'),
    path('video-comments/', views.video_comments, name='video_comments'),
    path('user-region/', views.user_region, name='user_region'),
    path('fans-analysis/', views.fans_analysis, name='fans_analysis'),
    path('comment-analysis/', views.comment_analysis, name='comment_analysis'),
    path('sentiment-analysis/', views.sentiment_analysis, name='sentiment_analysis'),
    path('comment-wordcloud/', views.comment_wordcloud, name='comment_wordcloud'),
    path('like-prediction/', views.like_prediction, name='like_prediction'),
    path('ai-suggestions/', views.ai_suggestions, name='ai_suggestions'),

    # API路由
    path('api/general-stats/', views.api_general_stats, name='api_general_stats'),
    path('api/like-collect-relation/', views.api_like_collect_relation, name='api_like_collect_relation'),
    path('api/fans-distribution/', views.api_fans_distribution, name='api_fans_distribution'),
    path('api/ip-distribution/', views.api_ip_distribution, name='api_ip_distribution'),
    path('api/top-users/', views.api_top_users, name='api_top_users'),
    path('api/top-videos/', views.api_top_videos, name='api_top_videos'),
    path('api/video-statistics/', views.api_video_statistics, name='api_video_statistics'),
    path('api/publish-time-distribution/', views.api_publish_time_distribution, name='api_publish_time_distribution'),
    path('api/full-report/', views.api_full_report, name='api_full_report'),
    path('api/video-list/', views.api_video_list, name='api_video_list'),
    path('api/video-comments/', views.api_video_comments, name='api_video_comments'),
    path('api/analyze-sentiment/', views.api_analyze_sentiment, name='api_analyze_sentiment'),
    path('api/clear-data/', views.api_clear_data, name='api_clear_data'),

    # 词云API
    path('api/video-wordcloud/', views.api_video_wordcloud, name='api_video_wordcloud'),
    path('api/comment-wordcloud/', views.api_comment_wordcloud, name='api_comment_wordcloud'),
    path('api/video-keywords/', views.api_video_keywords, name='api_video_keywords'),

    # AI分析API
    path('api/analyze-video-url/', views.api_analyze_video_url, name='api_analyze_video_url'),
    path('api/analyze-video-data/', views.api_analyze_video_data, name='api_analyze_video_data'),

    # 点赞数预测API
    path('api/prediction-stats/', views.api_prediction_stats, name='api_prediction_stats'),
    path('api/predict-likes/', views.api_predict_likes, name='api_predict_likes'),
    path('api/prediction-performance/', views.api_prediction_performance, name='api_prediction_performance'),
    path('api/prediction-comparison/', views.api_prediction_comparison, name='api_prediction_comparison'),

    # AI对话与分析API
    path('api/ai-chat/', views.api_ai_chat, name='api_ai_chat'),
    path('api/ai-analyze-video/', views.api_ai_analyze_video, name='api_ai_analyze_video'),
]
