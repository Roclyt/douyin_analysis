#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/15 0:24
# @Author  : Rocky

"""
数据存储模块 - 主要将CSV中的数据存储到MySQL数据库
"""

from typing import List, Dict, Optional
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
import os

import django
import sys

# 设置Django环境
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'douyin_analysis.settings')
django.setup()

from django.utils import timezone
from video.models import VideoData, CommentData
import config

logger = logging.getLogger(__name__)


class DataStorage:
    """数据存储类 - 从CSV读取数据并存储到MySQL"""

    def __init__(self):
        """初始化存储类"""
        # CSV文件路径
        self.video_csv_path = Path(__file__).parent / 'video_data.csv'
        self.comment_csv_path = Path(__file__).parent / 'comment.csv'

    @staticmethod
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

    @staticmethod
    def parse_datetime(datetime_str):
        """
        解析日期时间字符串
        支持多种格式
        """
        if pd.isna(datetime_str) or datetime_str == '':
            return timezone.now()

        datetime_str = str(datetime_str).strip()

        # 尝试多种日期格式
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S',
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%m-%d %H:%M',
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(datetime_str, fmt)
                return timezone.make_aware(dt)
            except ValueError:
                continue

        # 如果都不匹配，返回当前时间
        logger.warning(f"无法解析日期时间: {datetime_str}, 使用当前时间")
        return timezone.now()

    def load_video_from_csv(self, csv_path: Optional[str] = None) -> pd.DataFrame:
        """
        从CSV文件加载视频数据
        :param csv_path: CSV文件路径，默认使用video_data.csv
        :return: DataFrame
        """
        try:
            path = Path(csv_path) if csv_path else self.video_csv_path

            if not path.exists():
                logger.error(f"视频CSV文件不存在: {path}")
                return pd.DataFrame()

            df = pd.read_csv(path, encoding='utf-8')
            logger.info(f"成功加载视频CSV文件，共 {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"加载视频CSV文件失败: {e}")
            return pd.DataFrame()

    def load_comment_from_csv(self, csv_path: Optional[str] = None) -> pd.DataFrame:
        """
        从CSV文件加载评论数据
        :param csv_path: CSV文件路径，默认使用comment.csv
        :return: DataFrame
        """
        try:
            path = Path(csv_path) if csv_path else self.comment_csv_path

            if not path.exists():
                logger.error(f"评论CSV文件不存在: {path}")
                return pd.DataFrame()

            df = pd.read_csv(path, encoding='utf-8')
            logger.info(f"成功加载评论CSV文件，共 {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"加载评论CSV文件失败: {e}")
            return pd.DataFrame()

    def import_video_to_mysql(self, csv_path: Optional[str] = None,
                              batch_size: int = 100) -> Dict[str, int]:
        """
        从CSV文件导入视频数据到MySQL数据库
        :param csv_path: CSV文件路径
        :param batch_size: 批量插入的批次大小
        :return: 导入统计信息
        """
        stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'updated': 0,
            'created': 0
        }

        try:
            df = self.load_video_from_csv(csv_path)
            if df.empty:
                logger.warning("视频数据为空，跳过导入")
                return stats

            stats['total'] = len(df)

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
            df = df.rename(columns=column_mapping)

            # 数据预处理
            numeric_columns = ['fans_count', 'like_count', 'collect_count',
                               'comment_count', 'share_count']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            # 解析duration字段
            if 'duration' in df.columns:
                df['duration'] = df['duration'].apply(self.parse_duration)

            # 解析publish_time字段
            if 'publish_time' in df.columns:
                df['publish_time'] = df['publish_time'].apply(self.parse_datetime)

            # 批量导入
            logger.info(f"开始导入视频数据到MySQL数据库...")

            for idx, row in df.iterrows():
                try:
                    video_id = str(row['aweme_id']) if pd.notna(row['aweme_id']) else ''

                    if not video_id:
                        logger.warning(f"第 {idx + 1} 行缺少视频ID，跳过")
                        stats['failed'] += 1
                        continue

                    video_data = {
                        'awemeId': video_id,
                        'userName': str(row['user_name']) if pd.notna(row.get('user_name')) else '',
                        'fansCount': int(row['fans_count']) if pd.notna(row.get('fans_count')) else 0,
                        'description': str(row['description']) if pd.notna(row.get('description')) else '',
                        'publishTime': row['publish_time'] if pd.notna(row.get('publish_time')) else timezone.now(),
                        'duration': str(int(row['duration'])) if pd.notna(row.get('duration')) else '0',
                        'likeCount': int(row['like_count']) if pd.notna(row.get('like_count')) else 0,
                        'commentCount': str(int(row['comment_count'])) if pd.notna(row.get('comment_count')) else '0',
                        'shareCount': int(row['share_count']) if pd.notna(row.get('share_count')) else 0,
                        'collectCount': int(row['collect_count']) if pd.notna(row.get('collect_count')) else 0,
                    }

                    # 使用update_or_create避免重复
                    video, created = VideoData.objects.update_or_create(
                        awemeId=video_id,
                        defaults=video_data
                    )

                    if created:
                        stats['created'] += 1
                    else:
                        stats['updated'] += 1

                    stats['success'] += 1

                    # 每处理batch_size条记录输出一次日志
                    if (idx + 1) % batch_size == 0:
                        logger.info(f"已处理 {idx + 1}/{len(df)} 条视频数据")

                except Exception as e:
                    logger.error(f"导入第 {idx + 1} 行视频数据失败: {e}")
                    stats['failed'] += 1

            logger.info(f"视频数据导入完成: {stats}")
            return stats

        except Exception as e:
            logger.error(f"导入视频数据到MySQL失败: {e}")
            stats['failed'] = stats['total']
            return stats

    def import_comment_to_mysql(self, csv_path: Optional[str] = None,
                                batch_size: int = 100) -> Dict[str, int]:
        """
        从CSV文件导入评论数据到MySQL数据库
        :param csv_path: CSV文件路径
        :param batch_size: 批量插入的批次大小
        :return: 导入统计信息
        """
        stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
        }

        try:
            df = self.load_comment_from_csv(csv_path)
            if df.empty:
                logger.warning("评论数据为空，跳过导入")
                return stats

            stats['total'] = len(df)

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

            # 数据预处理
            if 'like_count' in df.columns:
                df['like_count'] = pd.to_numeric(df['like_count'], errors='coerce').fillna(0)

            # 解析comment_time字段
            if 'comment_time' in df.columns:
                df['comment_time'] = df['comment_time'].apply(self.parse_datetime)

            # 批量导入
            logger.info(f"开始导入评论数据到MySQL数据库...")

            for idx, row in df.iterrows():
                try:
                    video_id = str(row['aweme_id']) if pd.notna(row.get('aweme_id')) else ''
                    user_id = str(row['user_id']) if pd.notna(row.get('user_id')) else ''

                    if not video_id or not user_id:
                        logger.warning(f"第 {idx + 1} 行缺少视频ID或用户ID，跳过")
                        stats['failed'] += 1
                        continue

                    comment_data = {
                        'userId': int(user_id) if user_id.isdigit() else 0,
                        'userName': str(row['user_name']) if pd.notna(row.get('user_name')) else '',
                        'awemeId': video_id if video_id.isdigit() else 0,
                        'content': str(row['content']) if pd.notna(row.get('content')) else '',
                        'likeCount': int(row['like_count']) if pd.notna(row.get('like_count')) else 0,
                        'userIP': str(row['user_ip']) if pd.notna(row.get('user_ip')) else '',
                        'commentTime': row['comment_time'] if pd.notna(row.get('comment_time')) else timezone.now(),
                    }

                    # 创建评论
                    CommentData.objects.create(**comment_data)
                    stats['success'] += 1

                    # 每处理batch_size条记录输出一次日志
                    if (idx + 1) % batch_size == 0:
                        logger.info(f"已处理 {idx + 1}/{len(df)} 条评论数据")

                except Exception as e:
                    logger.error(f"导入第 {idx + 1} 行评论数据失败: {e}")
                    stats['failed'] += 1

            logger.info(f"评论数据导入完成: {stats}")
            return stats

        except Exception as e:
            logger.error(f"导入评论数据到MySQL失败: {e}")
            stats['failed'] = stats['total']
            return stats

    def import_all_to_mysql(self, video_csv: Optional[str] = None,
                            comment_csv: Optional[str] = None) -> Dict[str, Dict]:
        """
        从CSV文件导入所有数据到MySQL数据库
        :param video_csv: 视频CSV文件路径
        :param comment_csv: 评论CSV文件路径
        :return: 导入统计信息
        """
        results = {
            'video': {},
            'comment': {},
            'summary': {
                'total': 0,
                'success': 0,
                'failed': 0,
            }
        }

        logger.info("=" * 50)
        logger.info("开始导入CSV数据到MySQL数据库")
        logger.info("=" * 50)

        # 导入视频数据
        logger.info("\n1. 导入视频数据...")
        video_stats = self.import_video_to_mysql(video_csv)
        results['video'] = video_stats
        results['summary']['total'] += video_stats['total']
        results['summary']['success'] += video_stats['success']
        results['summary']['failed'] += video_stats['failed']

        # 导入评论数据
        logger.info("\n2. 导入评论数据...")
        comment_stats = self.import_comment_to_mysql(comment_csv)
        results['comment'] = comment_stats
        results['summary']['total'] += comment_stats['total']
        results['summary']['success'] += comment_stats['success']
        results['summary']['failed'] += comment_stats['failed']

        logger.info("\n" + "=" * 50)
        logger.info("数据导入完成")
        logger.info("=" * 50)
        logger.info(f"总计: {results['summary']['total']} 条")
        logger.info(f"成功: {results['summary']['success']} 条")
        logger.info(f"失败: {results['summary']['failed']} 条")

        return results

    @staticmethod
    def clear_all_data() -> Dict[str, int]:
        """
        清空所有数据（慎用）
        :return: 删除统计
        """
        logger.warning("开始清空所有数据...")

        video_count = VideoData.objects.count()
        comment_count = CommentData.objects.count()

        VideoData.objects.all().delete()
        CommentData.objects.all().delete()

        stats = {
            'videos_deleted': video_count,
            'comments_deleted': comment_count
        }

        logger.warning(f"数据清空完成: {stats}")
        return stats

    @staticmethod
    def get_database_stats() -> Dict[str, int]:
        """
        获取数据库统计信息
        :return: 统计信息
        """
        stats = {
            'video_count': VideoData.objects.count(),
            'comment_count': CommentData.objects.count(),
        }
        return stats


if __name__ == '__main__':
    # 测试存储功能
    storage = DataStorage()

    # 打印配置信息
    print("=" * 50)
    print("配置信息")
    print("=" * 50)
    print(f"数据库引擎: {config.Config.DB_ENGINE}")
    print(f"数据库主机: {config.Config.DB_HOST}")
    print(f"数据库名称: {config.Config.DB_NAME}")
    print(f"视频CSV路径: {storage.video_csv_path}")
    print(f"评论CSV路径: {storage.comment_csv_path}")

    # 获取数据库统计
    print("\n" + "=" * 50)
    print("数据库统计")
    print("=" * 50)
    stats = storage.get_database_stats()
    print(f"视频数: {stats['video_count']}")
    print(f"评论数: {stats['comment_count']}")

    # 询问是否导入数据
    print("\n" + "=" * 50)
    print("是否从CSV导入数据到MySQL数据库？")
    print("提示: 取消注释下面的代码来执行导入")
    print("=" * 50)

    # # 导入所有数据
    # results = storage.import_all_to_mysql()
    # print(f"\n导入结果: {results}")
