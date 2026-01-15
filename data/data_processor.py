#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/14 22:20
# @Author  : Rocky

"""
数据处理模块 - 使用Pandas进行数据清洗和处理
"""

import pandas as pd
import re
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """数据处理器类"""

    # 中文停用词列表
    STOP_WORDS = set([
        '的', '了', '和', '是', '在', '我', '有', '就', '不', '人', '都', '一',
        '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有',
        '看', '好', '自己', '这', '那', '个', '之', '与', '及', '等', '或', '但',
        '而', '因为', '所以', '如果', '虽然', '然而', '啊', '呀', '呢', '吧', '哦',
        '吗', '哈', '嘿', '嗯', '嗯嗯', '啦', '喔', '唉', '唉唉', '哎', '哎哎',
        '这个', '那个', '这种', '那种', '一些', '一下', '一下', '一直', '一般',
        '一起', '一下子', '一下下', '一会儿', '一旦', '一再', '一片', '一直',
        '一地', '一直', '一边', '一概', '一共', '一块', '一切', '一些', '一直',
        '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万',
        '亿', '零', '〇', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    ])

    @staticmethod
    def clean_text(text: str) -> str:
        """
        清洗文本数据
        :param text: 原始文本
        :return: 清洗后的文本
        """
        if not isinstance(text, str):
            return ''

        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)

        # 去除特殊字符，保留中文、英文、数字和基本标点
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、；：""''（）《》【】…— ]', '', text)

        # 去除多余空格和换行
        text = re.sub(r'\s+', ' ', text).strip()

        # 去除表情符号（简单处理）
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)

        return text

    @staticmethod
    def remove_stopwords(text: str) -> str:
        """
        去除停用词
        :param text: 文本
        :return: 去除停用词后的文本
        """
        if not isinstance(text, str):
            return ''

        words = text.split()
        filtered_words = [word for word in words if word not in DataProcessor.STOP_WORDS]
        return ' '.join(filtered_words)

    @classmethod
    def process_comment_text(cls, text: str) -> str:
        """
        处理评论文本（清洗+去停用词）
        :param text: 原始评论
        :return: 处理后的评论
        """
        text = cls.clean_text(text)
        text = cls.remove_stopwords(text)
        return text

    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """
        去除重复数据
        :param df: DataFrame
        :param subset: 判断重复的列名列表
        :return: 去重后的DataFrame
        """
        initial_count = len(df)
        df_cleaned = df.drop_duplicates(subset=subset, keep='last')
        removed_count = initial_count - len(df_cleaned)
        logger.info(f"去重前: {initial_count} 条, 去重后: {len(df_cleaned)} 条, 移除: {removed_count} 条")
        return df_cleaned

    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """
        处理缺失值
        :param df: DataFrame
        :return: 处理后的DataFrame
        """
        # 记录缺失值情况
        missing_info = df.isnull().sum()
        logger.info(f"缺失值统计:\n{missing_info}")

        # 数值型字段用0填充
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)

        # 文本型字段用空字符串填充
        text_columns = df.select_dtypes(include=['object']).columns
        df[text_columns] = df[text_columns].fillna('')

        return df

    @staticmethod
    def filter_by_value(df: pd.DataFrame, column: str, min_val: float = None, max_val: float = None) -> pd.DataFrame:
        """
        根据数值范围过滤数据
        :param df: DataFrame
        :param column: 列名
        :param min_val: 最小值
        :param max_val: 最大值
        :return: 过滤后的DataFrame
        """
        if min_val is not None:
            df = df[df[column] >= min_val]
        if max_val is not None:
            df = df[df[column] <= max_val]
        return df

    @staticmethod
    def categorize_followers(followers_count: int) -> str:
        """
        将粉丝数分类
        :param followers_count: 粉丝数
        :return: 分类标签
        """
        if followers_count < 1000:
            return '普通用户(0-1k)'
        elif followers_count < 10000:
            return '小V(1k-1w)'
        elif followers_count < 100000:
            return '中V(1w-10w)'
        elif followers_count < 1000000:
            return '大V(10w-100w)'
        else:
            return '超V(100w+)'

    @staticmethod
    def convert_to_dataframe(data: List[Dict]) -> pd.DataFrame:
        """
        将字典列表转换为DataFrame
        :param data: 字典列表
        :return: DataFrame
        """
        return pd.DataFrame(data)

    @staticmethod
    def process_user_data(users_df: pd.DataFrame) -> pd.DataFrame:
        """
        处理用户数据
        :param users_df: 用户DataFrame
        :return: 处理后的用户DataFrame
        """
        logger.info("开始处理用户数据...")

        # 去重（基于user_id）
        users_df = DataProcessor.remove_duplicates(users_df, subset=['user_id'])

        # 处理缺失值
        users_df = DataProcessor.handle_missing_values(users_df)

        # 清洗昵称和位置
        users_df['nickname'] = users_df['nickname'].apply(DataProcessor.clean_text)
        users_df['ip_location'] = users_df['ip_location'].apply(DataProcessor.clean_text)

        # 添加粉丝分类
        users_df['followers_category'] = users_df['followers_count'].apply(DataProcessor.categorize_followers)

        logger.info(f"用户数据处理完成，共 {len(users_df)} 条记录")
        return users_df

    @staticmethod
    def process_video_data(videos_df: pd.DataFrame) -> pd.DataFrame:
        """
        处理视频数据
        :param videos_df: 视频DataFrame
        :return: 处理后的视频DataFrame
        """
        logger.info("开始处理视频数据...")

        # 去重（基于video_id）
        videos_df = DataProcessor.remove_duplicates(videos_df, subset=['video_id'])

        # 处理缺失值
        videos_df = DataProcessor.handle_missing_values(videos_df)

        # 清洗标题和描述
        videos_df['title'] = videos_df['title'].apply(DataProcessor.clean_text)
        videos_df['description'] = videos_df['description'].apply(DataProcessor.clean_text)

        # 确保数值型字段为非负数
        numeric_columns = ['view_count', 'like_count', 'comment_count', 'share_count', 'collect_count']
        for col in numeric_columns:
            if col in videos_df.columns:
                videos_df[col] = videos_df[col].apply(lambda x: max(0, x))

        # 重新计算互动率
        total_interaction = (
            videos_df['like_count'] + videos_df['comment_count'] +
            videos_df['share_count'] + videos_df['collect_count']
        )
        videos_df['interaction_rate'] = total_interaction / videos_df['view_count'].replace(0, 1)

        logger.info(f"视频数据处理完成，共 {len(videos_df)} 条记录")
        return videos_df

    @staticmethod
    def process_comment_data(comments_df: pd.DataFrame) -> pd.DataFrame:
        """
        处理评论数据
        :param comments_df: 评论DataFrame
        :return: 处理后的评论DataFrame
        """
        logger.info("开始处理评论数据...")

        # 去重（基于comment_id）
        comments_df = DataProcessor.remove_duplicates(comments_df, subset=['comment_id'])

        # 处理缺失值
        comments_df = DataProcessor.handle_missing_values(comments_df)

        # 清洗评论文本
        comments_df['content'] = comments_df['content'].apply(DataProcessor.process_comment_text)

        # 过滤空评论
        comments_df = comments_df[comments_df['content'].str.len() > 0]

        # 确保数值型字段为非负数
        if 'like_count' in comments_df.columns:
            comments_df['like_count'] = comments_df['like_count'].apply(lambda x: max(0, x))
        if 'reply_count' in comments_df.columns:
            comments_df['reply_count'] = comments_df['reply_count'].apply(lambda x: max(0, x))

        logger.info(f"评论数据处理完成，共 {len(comments_df)} 条记录")
        return comments_df


def save_dataframe_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """
    将DataFrame保存为CSV文件
    :param df: DataFrame
    :param filepath: 文件路径
    """
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    logger.info(f"数据已保存到 {filepath}")


if __name__ == '__main__':

    processor = DataProcessor()

    print("原始数据:")



