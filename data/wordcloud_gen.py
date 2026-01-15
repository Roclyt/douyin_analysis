#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/15 9:51
# @Author  : Rocky

"""
词云生成模块
"""

from wordcloud import WordCloud
import jieba
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import logging
from typing import List, Dict
import re
from collections import Counter
import sys
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import os
import uuid
import pandas as pd

# 导入config
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

from video.models import VideoData, CommentData

# CSV文件路径
COMMENT_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'comment.csv')

logger = logging.getLogger(__name__)


class WordCloudGenerator:
    """词云生成类"""

    # 静态文件保存路径
    STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

    # 停用词
    STOP_WORDS = set([
        '的', '了', '和', '是', '在', '我', '有', '就', '不', '人', '都', '一',
        '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有',
        '看', '好', '自己', '这', '那', '个', '之', '与', '及', '等', '或', '但',
        '而', '因为', '所以', '如果', '虽然', '然而', '啊', '呀', '呢', '吧', '哦',
        '吗', '哈', '嘿', '嗯', '嗯嗯', '啦', '喔', '唉', '唉唉', '哎', '哎哎',
        '这个', '那个', '这种', '那种', '一些', '一下', '一下', '一直', '一般',
        '一起', '一下子', '一旦', '一再', '一片', '一直', '一地', '一直', '一边',
        '一概', '一共', '一块', '一切', '一些', '一直', '抖音', '视频', '链接',
        '分享', '评论', '点赞', '收藏', '关注', '我们', '你们', '他们', '它们'
    ])

    @staticmethod
    def load_comment_data_from_csv(video_id: str = None) -> pd.DataFrame:
        """
        从CSV文件加载评论数据
        :param video_id: 视频ID，None表示所有评论
        :return: DataFrame
        """
        try:
            if not os.path.exists(COMMENT_CSV_PATH):
                logger.warning(f"评论CSV文件不存在: {COMMENT_CSV_PATH}")
                return pd.DataFrame()

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

            # 根据video_id筛选
            if video_id is not None:
                df['aweme_id'] = df['aweme_id'].astype(str)
                video_id_str = str(video_id)
                df = df[df['aweme_id'] == video_id_str]

            return df
        except Exception as e:
            logger.error(f"从CSV加载评论数据失败: {e}")
            return pd.DataFrame()

    @staticmethod
    def create_heart_mask(width: int = 800, height: int = 600) -> np.ndarray:
        """
        创建爱心形状的mask
        :param width: 图片宽度
        :param height: 图片高度
        :return: mask数组
        """
        # 创建空白图像
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)

        # 爱心参数
        center_x, center_y = width // 2, height // 2
        scale = min(width, height) // 30

        # 创建爱心形状
        # 使用参数方程创建爱心
        for t in np.linspace(0, 2 * np.pi, 500):
            # 爱心参数方程
            x = 16 * np.sin(t) ** 3
            y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

            # 转换到图像坐标
            px = int(center_x + x * scale)
            py = int(center_y - y * scale)  # y轴翻转

            # 绘制点
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=255)

        # 填充爱心内部
        mask_array = np.array(mask)

        # 创建填充版本
        mask_filled = mask_array.copy()
        from scipy.ndimage import binary_fill_holes
        mask_filled = binary_fill_holes(mask_array).astype(np.uint8) * 255

        # 平滑边缘
        from scipy.ndimage import gaussian_filter
        mask_smooth = gaussian_filter(mask_filled, sigma=2)

        return mask_smooth

    @staticmethod
    def clean_text(text: str) -> str:
        """
        清洗文本
        :param text: 原始文本
        :return: 清洗后的文本
        """
        if not isinstance(text, str):
            return ''

        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)

        # 去除特殊字符，保留中文、英文、数字
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)

        # 去除多余空格
        text = re.sub(r'\s+', '', text).strip()

        return text

    @classmethod
    def segment_text(cls, text: str) -> List[str]:
        """
        使用jieba分词
        :param text: 文本
        :return: 分词列表
        """
        text = cls.clean_text(text)

        if not text:
            return []

        # 使用jieba分词
        words = jieba.lcut(text)

        # 过滤停用词和短词
        filtered_words = [
            word for word in words
            if len(word) > 1  # 至少2个字符
            and word not in cls.STOP_WORDS
            and word.strip()  # 非空字符串
        ]

        return filtered_words

    @classmethod
    def generate_video_wordcloud(cls, video_id: str = None) -> Dict:
        """
        生成视频描述的词云
        :param video_id: 视频ID，None表示所有视频
        :return: 词云数据
        """
        try:
            # 获取视频数据
            if video_id:
                videos = VideoData.objects.filter(awemeId=video_id)
            else:
                videos = VideoData.objects.all()

            if videos.count() == 0:
                return {
                    'success': False,
                    'message': '没有找到视频数据'
                }

            # 收集所有描述文本
            all_words = []
            for video in videos:
                words = cls.segment_text(video.description)
                all_words.extend(words)

            if not all_words:
                return {
                    'success': False,
                    'message': '没有可用的关键词'
                }

            # 生成词云
            wordcloud = cls._create_wordcloud_image(all_words)

            # 统计词频
            word_freq = Counter(all_words)
            top_words = word_freq.most_common(50)

            return {
                'success': True,
                'image': wordcloud,
                'top_words': top_words,
                'total_words': len(all_words),
                'video_count': videos.count()
            }

        except Exception as e:
            logger.error(f"生成视频词云失败: {e}")
            return {
                'success': False,
                'message': f'生成失败: {str(e)}'
            }

    @classmethod
    def generate_comment_wordcloud(cls, video_id: str = None) -> Dict:
        """
        生成评论内容的词云
        :param video_id: 视频ID，None表示所有评论
        :return: 词云数据
        """
        try:
            # 从CSV文件加载评论数据
            df = cls.load_comment_data_from_csv(video_id)

            if df.empty:
                return {
                    'success': False,
                    'message': '没有找到评论数据'
                }

            # 收集所有评论文本
            all_words = []
            for content in df['content']:
                if pd.notna(content) and isinstance(content, str):
                    words = cls.segment_text(content)
                    all_words.extend(words)

            if not all_words:
                return {
                    'success': False,
                    'message': '没有可用的关键词'
                }

            # 生成词云
            wordcloud = cls._create_wordcloud_image(all_words, shape='heart', save_to_static=True, video_id=video_id)

            # 统计词频（返回所有关键词，用于详细统计）
            word_freq = Counter(all_words)
            keywords = [
                {'word': word, 'count': count}
                for word, count in word_freq.most_common()
            ]

            return {
                'success': True,
                'image': wordcloud,
                'keywords': keywords,
                'total_words': len(all_words),
                'comment_count': len(df)
            }

        except Exception as e:
            logger.error(f"生成评论词云失败: {e}")
            return {
                'success': False,
                'message': f'生成失败: {str(e)}'
            }

    @staticmethod
    def _create_wordcloud_image(words: List[str], shape: str = 'default', save_to_static: bool = False, video_id: str = None) -> str:
        """
        创建词云图片并转为base64
        :param words: 词列表
        :param shape: 形状类型（'default', 'heart'）
        :param save_to_static: 是否保存到static文件夹
        :param video_id: 视频ID（用于生成文件名）
        :return: base64编码的图片
        """
        if not words:
            return ''

        # 将词列表转为字符串，用空格分隔
        text = ' '.join(words)

        # 获取字体路径
        font_path = config.get_font_path()

        # 生成mask（如果是爱心形状）
        mask = None
        if shape == 'heart':
            mask = WordCloudGenerator.create_heart_mask()

        # 生成词云
        wordcloud = WordCloud(
            width=800,
            height=600,
            background_color='white',
            font_path=font_path,  # 使用配置文件中的字体路径
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10,
            mask=mask,
            contour_width=0 if shape != 'heart' else 1,
            contour_color='red' if shape == 'heart' else None,
            collocations=False
        ).generate(text)

        # 保存到内存
        buf = BytesIO()
        plt.figure(figsize=(10, 7.5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', transparent=(shape == 'heart'))
        plt.close()

        # 保存到static文件夹
        if save_to_static:
            # 确保static文件夹存在
            os.makedirs(WordCloudGenerator.STATIC_DIR, exist_ok=True)

            # 生成文件名
            if video_id:
                filename = f"wordcloud_{video_id}.png"
            else:
                filename = f"wordcloud_{uuid.uuid4().hex[:8]}.png"

            filepath = os.path.join(WordCloudGenerator.STATIC_DIR, filename)

            # 保存图片
            with open(filepath, 'wb') as f:
                f.write(buf.getvalue())

            logger.info(f"词云图片已保存到: {filepath}")

        # 转为base64
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        return f'data:image/png;base64,{image_base64}'

    @staticmethod
    def get_word_frequency(words: List[str], top_n: int = 30) -> List[Dict]:
        """
        获取词频统计
        :param words: 词列表
        :param top_n: 返回前N个词
        :return: 词频列表
        """
        word_freq = Counter(words)
        top_words = word_freq.most_common(top_n)

        return [
            {
                'word': word,
                'count': count
            }
            for word, count in top_words
        ]

    @classmethod
    def analyze_video_keywords(cls, video_id: str) -> Dict:
        """
        分析单个视频的关键词
        :param video_id: 视频ID
        :return: 分析结果
        """
        try:
            video = VideoData.objects.get(aweme_id=video_id)
            comments = CommentData.objects.filter(aweme_id=video_id)

            # 描述关键词
            desc_words = cls.segment_text(video.description)

            # 评论文本关键词
            comment_words = []
            for comment in comments:
                words = cls.segment_text(comment.content)
                comment_words.extend(words)

            # 统计
            desc_freq = Counter(desc_words).most_common(20)
            comment_freq = Counter(comment_words).most_common(20)

            return {
                'success': True,
                'video_id': video_id,
                'description_keywords': [
                    {'word': word, 'count': count}
                    for word, count in desc_freq
                ],
                'comment_keywords': [
                    {'word': word, 'count': count}
                    for word, count in comment_freq
                ],
                'comment_count': comments.count()
            }

        except VideoData.DoesNotExist:
            return {
                'success': False,
                'message': f'视频不存在: {video_id}'
            }
        except Exception as e:
            logger.error(f"分析视频关键词失败: {e}")
            return {
                'success': False,
                'message': f'分析失败: {str(e)}'
            }
