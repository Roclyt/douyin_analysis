"""
数据分析模块 - 使用Pandas进行数据分析
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# CSV文件路径
VIDEO_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'video_data.csv')
COMMENT_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'comment.csv')


def parse_duration(duration_str):
    """
    解析视频时长字符串，转换为秒数
    例如: "01:59" -> 119秒
    """
    try:
        if pd.isna(duration_str) or duration_str == '':
            return 0
        duration_str = str(duration_str).strip()
        parts = duration_str.split(':')
        if len(parts) == 2:
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes * 60 + seconds
        elif len(parts) == 3:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        return 0
    except:
        return 0


class DataAnalyzer:
    """数据分析类"""

    @staticmethod
    def _load_data():
        """
        从CSV文件加载数据到DataFrame
        :return: (video_data, comment_data)
        """
        try:
            # 读取视频CSV
            if os.path.exists(VIDEO_CSV_PATH):
                video_data = pd.read_csv(VIDEO_CSV_PATH, encoding='utf-8')

                # 列名映射
                column_mapping = {
                    '用户名': 'user_name',
                    '粉丝数量': 'fans_count',
                    '视频描述': 'description',
                    '发布时间': 'publish_time',
                    '视频时长': 'duration',
                    '点赞数': 'like_count',
                    '收藏数': 'collect_count',
                    '评论数': 'comment_count',
                    '分享数': 'share_count',
                    '视频ID': 'aweme_id'
                }

                # 重命名列
                video_data = video_data.rename(columns=column_mapping)

                # 数据类型转换
                numeric_columns = ['fans_count', 'like_count', 'collect_count', 'comment_count', 'share_count']
                for col in numeric_columns:
                    if col in video_data.columns:
                        video_data[col] = pd.to_numeric(video_data[col], errors='coerce').fillna(0)

                # 将aweme_id转换为字符串，便于API查找
                if 'aweme_id' in video_data.columns:
                    video_data['aweme_id'] = video_data['aweme_id'].astype(str)

                # 解析duration字段
                if 'duration' in video_data.columns:
                    video_data['duration'] = video_data['duration'].apply(parse_duration)

            else:
                logger.warning(f"视频CSV文件不存在: {VIDEO_CSV_PATH}")
                video_data = pd.DataFrame()

            # 读取评论CSV
            if os.path.exists(COMMENT_CSV_PATH):
                comment_data = pd.read_csv(COMMENT_CSV_PATH, encoding='utf-8')

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
                comment_data = comment_data.rename(columns=column_mapping)

                # 数据类型转换
                if 'like_count' in comment_data.columns:
                    comment_data['like_count'] = pd.to_numeric(comment_data['like_count'], errors='coerce').fillna(0)

                # 将aweme_id转换为字符串，便于API查找
                if 'aweme_id' in comment_data.columns:
                    comment_data['aweme_id'] = comment_data['aweme_id'].astype(str)
            else:
                logger.warning(f"评论CSV文件不存在: {COMMENT_CSV_PATH}")
                comment_data = pd.DataFrame()

            logger.info(f"从CSV加载数据: 视频 {len(video_data)} 条, 评论 {len(comment_data)} 条")
            return video_data, comment_data

        except Exception as e:
            logger.error(f"从CSV加载数据失败: {e}")
            return pd.DataFrame(), pd.DataFrame()

    @staticmethod
    def analyze_user_ip_distribution() -> Dict[str, int]:
        """
        统计IP地址分布 (part1)
        :return: IP分布字典
        """
        try:
            _, comment_data = DataAnalyzer._load_data()

            if comment_data.empty or 'user_ip' not in comment_data.columns:
                logger.warning("暂无评论数据或user_ip字段不存在")
                return {}

            # 统计IP地址
            result = comment_data['user_ip'].value_counts().reset_index()
            result.columns = ['user_ip', 'count']

            # 取前10个IP
            result = result.head(10).set_index('user_ip')['count'].to_dict()

            logger.info(f"IP地址分布统计完成，共 {len(result)} 个IP")
            return result
        except Exception as e:
            logger.error(f"统计IP地址失败: {e}")
            return {}

    @staticmethod
    def analyze_like_collect_relation() -> Dict[str, any]:
        """
        统计点赞数和收藏 (part2)
        :return: 分析结果
        """
        try:
            video_data, _ = DataAnalyzer._load_data()

            if video_data.empty or 'like_count' not in video_data.columns or 'collect_count' not in video_data.columns:
                logger.warning("暂无视频数据或字段不存在")
                return {}

            # 获取点赞数前10的视频
            result = video_data[['like_count', 'collect_count', 'description']] \
                .sort_values('like_count', ascending=False) \
                .head(10)

            # 计算收藏/点赞比
            result['ratio'] = (result['collect_count'] / result['like_count']).round(4)

            # 转换为字典格式
            result_dict = result[['description', 'like_count', 'collect_count', 'ratio']].to_dict('records')

            logger.info(f"点赞收藏关系统计完成，共 {len(result_dict)} 条数据")
            return {'data': result_dict}
        except Exception as e:
            logger.error(f"统计点赞收藏失败: {e}")
            return {}

    @staticmethod
    def categorize_fans_distribution() -> Dict[str, int]:
        """
        粉丝数量区间 (part3)
        :return: 粉丝区间分布
        """
        try:
            video_data, _ = DataAnalyzer._load_data()

            if video_data.empty or 'fans_count' not in video_data.columns:
                logger.warning("暂无视频数据或fans_count字段不存在")
                return {}

            # 定义区间
            bins = [-1, 100, 1000, 10000, 100000, float('inf')]
            labels = ['0-99', '100-999', '1000-9999', '10000-99999', '100000+']

            # 分类
            video_data['fans_range'] = pd.cut(video_data['fans_count'], bins=bins, labels=labels)

            # 统计
            result = video_data['fans_range'].value_counts().reset_index()
            result.columns = ['range', 'count']

            # 转换为字典
            result_dict = result.set_index('range')['count'].to_dict()

            logger.info(f"粉丝数量区间统计完成，共 {len(result_dict)} 个区间")
            return result_dict
        except Exception as e:
            logger.error(f"统计粉丝数量区间失败: {e}")
            return {}

    @staticmethod
    def get_top_users_by_fans(limit: int = 10) -> List[Dict]:
        """
        粉丝数量排行 (part4)
        :param limit: 返回数量
        :return: 用户排行列表
        """
        try:
            video_data, _ = DataAnalyzer._load_data()

            if video_data.empty or 'user_name' not in video_data.columns or 'fans_count' not in video_data.columns:
                logger.warning("暂无视频数据或字段不存在")
                return []

            # 去重并排序
            result = video_data[['user_name', 'fans_count']] \
                .drop_duplicates('user_name') \
                .sort_values('fans_count', ascending=False) \
                .head(limit)

            # 转换为字典列表
            result_list = result.to_dict('records')

            logger.info(f"粉丝数量排行完成，前 {len(result_list)} 名")
            return result_list
        except Exception as e:
            logger.error(f"统计粉丝数量排行失败: {e}")
            return []

    @staticmethod
    def get_top_videos_by_likes(limit: int = 10) -> List[Dict]:
        """
        获取热门视频排行（按点赞数）
        :param limit: 返回数量
        :return: 视频列表
        """
        try:
            video_data, _ = DataAnalyzer._load_data()

            if video_data.empty or 'like_count' not in video_data.columns:
                logger.warning("暂无视频数据或like_count字段不存在")
                return []

            # 按点赞数排序
            result = video_data[['aweme_id', 'user_name', 'description', 'like_count', 'comment_count', 'share_count', 'collect_count']] \
                .sort_values('like_count', ascending=False) \
                .head(limit)

            # 转换为字典列表
            result_list = result.to_dict('records')

            logger.info(f"热门视频排行完成，共 {len(result_list)} 条数据")
            return result_list
        except Exception as e:
            logger.error(f"统计热门视频失败: {e}")
            return []

    @staticmethod
    def analyze_video_statistics() -> Dict[str, any]:
        """
        分析视频统计数据
        :return: 统计结果
        """
        try:
            video_data, _ = DataAnalyzer._load_data()

            if video_data.empty:
                return {}

            numeric_columns = ['comment_count', 'like_count', 'share_count', 'collect_count']
            stats = {}

            for col in numeric_columns:
                if col in video_data.columns:
                    stats[col] = {
                        'total': int(video_data[col].sum()),
                        'mean': float(video_data[col].mean()),
                        'max': int(video_data[col].max()),
                        'min': int(video_data[col].min()),
                        'median': float(video_data[col].median())
                    }

            logger.info("视频统计分析完成")
            return stats
        except Exception as e:
            logger.error(f"视频统计分析失败: {e}")
            return {}

    @staticmethod
    def analyze_publish_time_distribution() -> Dict[str, int]:
        """
        分析视频发布时间分布（按小时）
        :return: 时间分布
        """
        try:
            video_data, _ = DataAnalyzer._load_data()

            if video_data.empty or 'publish_time' not in video_data.columns:
                return {}

            # 提取小时
            video_data['publish_hour'] = pd.to_datetime(video_data['publish_time']).dt.hour

            # 统计各小时的视频数量
            time_distribution = video_data['publish_hour'].value_counts().sort_index().to_dict()

            result = {str(k): int(v) for k, v in time_distribution.items()}

            logger.info(f"发布时间分布分析完成")
            return result
        except Exception as e:
            logger.error(f"发布时间分布分析失败: {e}")
            return {}

    @staticmethod
    def get_general_statistics() -> Dict[str, int]:
        """
        获取总体统计数据
        :return: 统计数据
        """
        try:
            video_data, comment_data = DataAnalyzer._load_data()

            total_videos = len(video_data) if not video_data.empty else 0
            total_comments = len(comment_data) if not comment_data.empty else 0

            return {
                'total_videos': total_videos,
                'total_comments': total_comments,
            }
        except Exception as e:
            logger.error(f"获取总体统计数据失败: {e}")
            return {
                'total_videos': 0,
                'total_comments': 0,
            }

    @staticmethod
    def generate_full_analysis_report() -> Dict[str, any]:
        """
        生成完整的分析报告
        :return: 分析报告
        """
        logger.info("开始生成完整分析报告...")

        report = {
            'general_statistics': DataAnalyzer.get_general_statistics(),
            'user_ip_distribution': DataAnalyzer.analyze_user_ip_distribution(),
            'like_collect_relation': DataAnalyzer.analyze_like_collect_relation(),
            'fans_distribution': DataAnalyzer.categorize_fans_distribution(),
            'top_users': DataAnalyzer.get_top_users_by_fans(limit=10),
            'top_videos': DataAnalyzer.get_top_videos_by_likes(limit=10),
            'video_statistics': DataAnalyzer.analyze_video_statistics(),
            'publish_time_distribution': DataAnalyzer.analyze_publish_time_distribution(),
        }

        logger.info("完整分析报告生成完成")
        return report
