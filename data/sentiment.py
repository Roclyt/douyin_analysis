#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/14 23:41
# @Author  : Rocky
"""
SnowNLP情感分析模块
"""

import logging
import pandas as pd
import os
from typing import Dict, List, Tuple
from snownlp import SnowNLP

from video.models import CommentData

logger = logging.getLogger(__name__)

# CSV文件路径
COMMENT_CSV_PATH = os.path.join(os.path.dirname(__file__), 'comment.csv')


class SentimentAnalyzer:
    """情感分析类"""

    # 情感阈值
    POSITIVE_THRESHOLD = 0.6
    NEGATIVE_THRESHOLD = 0.4

    @staticmethod
    def load_comments_from_csv():
        """
        从CSV文件加载评论数据
        :return: DataFrame
        """
        try:
            if os.path.exists(COMMENT_CSV_PATH):
                df = pd.read_csv(COMMENT_CSV_PATH, encoding='utf-8')

                # 列名映射
                column_mapping = {
                    '用户id': 'user_id',
                    '用户名': 'user_name',
                    '评论内容': 'content',
                    '评论时间': 'comment_time',
                    'IP地址': 'user_ip',
                    '点赞数': 'like_count',
                    '视频id': 'aweme_id'
                }

                # 重命名列
                df = df.rename(columns=column_mapping)

                # 数据类型转换
                if 'like_count' in df.columns:
                    df['like_count'] = pd.to_numeric(df['like_count'], errors='coerce').fillna(0)

                return df
            else:
                logger.warning(f"评论CSV文件不存在: {COMMENT_CSV_PATH}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"从CSV加载评论数据失败: {e}")
            return pd.DataFrame()

    @staticmethod
    def analyze_text(text: str) -> Tuple[float, str]:
        """
        分析文本情感
        :param text: 文本内容
        :return: (情感得分, 情感标签)
        """
        if not text or not isinstance(text, str):
            return 0.0, 'neutral'

        try:
            s = SnowNLP(text)
            score = s.sentiments

            # 根据得分确定情感标签
            if score >= SentimentAnalyzer.POSITIVE_THRESHOLD:
                label = 'positive'
            elif score <= SentimentAnalyzer.NEGATIVE_THRESHOLD:
                label = 'negative'
            else:
                label = 'neutral'

            return round(score, 4), label

        except Exception as e:
            logger.error(f"情感分析失败: {e}")
            return 0.0, 'neutral'

    @staticmethod
    def analyze_comment(comment: CommentData) -> Dict[str, any]:
        """
        分析单条评论的情感
        :param comment: CommentData实例
        :return: 分析结果
        """
        score, label = SentimentAnalyzer.analyze_text(comment.content)

        # 更新评论的情感信息
        comment.sentiment_score = score
        comment.sentiment_label = label
        comment.save()

        result = {
            'comment_id': comment.id,
            'content': comment.content,
            'sentiment_score': score,
            'sentiment_label': label
        }

        return result

    @staticmethod
    def analyze_all_comments() -> Dict[str, any]:
        """
        分析所有评论的情感
        :return: 统计结果
        """
        logger.info("开始分析所有评论情感...")

        # 从CSV加载评论数据
        df = SentimentAnalyzer.load_comments_from_csv()

        if df.empty:
            logger.warning("暂无评论数据")
            return {
                'total': 0,
                'analyzed': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'average_score': 0.0,
                'comments': []
            }

        total = len(df)
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_score = 0.0
        analyzed_count = 0
        comments_list = []

        for _, row in df.iterrows():
            content = row['content'] if pd.notna(row['content']) else ''
            score, label = SentimentAnalyzer.analyze_text(str(content))

            # 收集评论列表（取前100条）
            if len(comments_list) < 100:
                comments_list.append({
                    'content': str(content),
                    'sentiment': score,
                    'user_name': str(row['user_name']) if pd.notna(row['user_name']) else ''
                })

            # 统计
            if label == 'positive':
                positive_count += 1
            elif label == 'negative':
                negative_count += 1
            else:
                neutral_count += 1

            total_score += score
            analyzed_count += 1

        result = {
            'total': total,
            'analyzed': analyzed_count,
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'average_score': round(total_score / analyzed_count, 4) if analyzed_count > 0 else 0.0,
            'comments': comments_list
        }

        logger.info(f"评论情感分析完成: {result}")
        return result

    @staticmethod
    def analyze_comments_by_video(video_id: str) -> Dict[str, any]:
        """
        分析指定视频的评论情感
        :param video_id: 视频ID
        :return: 统计结果
        """
        logger.info(f"开始分析视频 {video_id} 的评论情感...")

        # 从CSV加载评论数据
        df = SentimentAnalyzer.load_comments_from_csv()

        if df.empty:
            logger.warning("暂无评论数据")
            return {
                'total': 0,
                'analyzed': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'average_score': 0.0,
                'comments': []
            }

        # 筛选指定视频的评论
        df['aweme_id'] = df['aweme_id'].astype(str)
        df_video = df[df['aweme_id'] == str(video_id)]

        if df_video.empty:
            logger.warning(f"视频 {video_id} 没有评论数据")
            return {
                'total': 0,
                'analyzed': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'average_score': 0.0,
                'comments': []
            }

        total = len(df_video)
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_score = 0.0
        analyzed_count = 0
        comments_list = []

        for _, row in df_video.iterrows():
            content = row['content'] if pd.notna(row['content']) else ''
            score, label = SentimentAnalyzer.analyze_text(str(content))

            # 收集评论列表（最多100条）
            if len(comments_list) < 100:
                comments_list.append({
                    'content': str(content),
                    'sentiment': score,
                    'user_name': str(row['user_name']) if pd.notna(row['user_name']) else ''
                })

            # 统计
            if label == 'positive':
                positive_count += 1
            elif label == 'negative':
                negative_count += 1
            else:
                neutral_count += 1

            total_score += score
            analyzed_count += 1

        result = {
            'total': total,
            'analyzed': analyzed_count,
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'average_score': round(total_score / analyzed_count, 4) if analyzed_count > 0 else 0.0,
            'comments': comments_list
        }

        logger.info(f"视频 {video_id} 的评论情感分析完成: {result}")
        return result

    @staticmethod
    def analyze_comments_batch(comment_ids: List[str]) -> List[Dict]:
        """
        批量分析评论情感
        :param comment_ids: 评论ID列表
        :return: 分析结果列表
        """
        results = []

        for comment_id in comment_ids:
            try:
                comment = CommentData.objects.get(id=comment_id)
                result = SentimentAnalyzer.analyze_comment(comment)
                results.append(result)
            except CommentData.DoesNotExist:
                logger.warning(f"评论不存在: {comment_id}")

        return results

    @staticmethod
    def get_sentiment_summary() -> Dict[str, any]:
        """
        获取情感分析摘要
        :return: 摘要数据
        """
        comments = CommentData.objects.all()

        if comments.count() == 0:
            return {
                'total': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'average_score': 0.0,
                'distribution': {}
            }

        # 统计情感分布
        positive_count = comments.filter(sentiment_label='positive').count()
        negative_count = comments.filter(sentiment_label='negative').count()
        neutral_count = comments.filter(sentiment_label='neutral').count()

        # 计算平均得分
        avg_score = comments.aggregate(avg_score=Avg('sentiment_score'))['avg_score'] or 0.0

        result = {
            'total': comments.count(),
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'average_score': round(float(avg_score), 4),
            'distribution': {
                'positive': positive_count,
                'negative': negative_count,
                'neutral': neutral_count
            }
        }

        return result

    @staticmethod
    def get_positive_comments(limit: int = 10) -> List[CommentData]:
        """获取积极评论"""
        return list(CommentData.objects.filter(sentiment_label='positive')
                    .order_by('-sentiment_score')[:limit])

    @staticmethod
    def get_negative_comments(limit: int = 10) -> List[CommentData]:
        """获取消极评论"""
        return list(CommentData.objects.filter(sentiment_label='negative')
                    .order_by('sentiment_score')[:limit])


from django.db.models import Avg


if __name__ == '__main__':
    # 测试情感分析
    test_texts = [
        "太棒了！非常喜欢！",
        "不好，很失望",
        "一般般吧",
        "这个视频很有趣，学到了很多！",
        "浪费时间，不推荐"
    ]

    for text in test_texts:
        score, label = SentimentAnalyzer.analyze_text(text)
        print(f"{text}: 得分={score}, 标签={label}")
