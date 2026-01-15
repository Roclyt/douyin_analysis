#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/3 22:13
# @Author  : Rocky

# import pandas as pd
# import pymysql
# from config import Config

# conn = pymysql.connect(
#     host=Config.DB_HOST,
#     user=Config.DB_USER,
#     password=Config.DB_PASSWORD,
#     db=Config.DB_NAME,
#     port=Config.DB_PORT,
#     # charset='utf8'
# )
#
# cursor = conn.cursor()
#
# # 存储视频信息
# def save_video_info():
#     sql = 'insert into video_data (userName, fansCount, description, awemeId, publishTime,' \
#             'duration, commentCount, likeCount, shareCount, collectCount)' \
#             'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#
#     df = pd.read_csv('video_data.csv')
#     for index, row in df.iterrows():
#         cursor.execute(sql, tuple(row))
#     conn.commit()
#     cursor.close()
#     conn.close()
#
# save_video_info()
#
# # 存储评论信息
# def save_comment_info():
#     sql = 'insert into comment_data (userId, userName, commentTime, userIP, content, likeCount, awemeId)' \
#             'values (%s, %s, %s, %s, %s, %s, %s)'
#
#     df = pd.read_csv('comment.csv')
#     # 删除空行
#     df = df.dropna(subset=['评论内容'])
#     for index, row in df.iterrows():
#         cursor.execute(sql, tuple(row))
#     conn.commit()
#     cursor.close()
#     conn.close()
#
# save_comment_info()


import pandas as pd
import os
import logging
from video.models import VideoData, CommentData
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


def parse_publish_time(time_str):
    """
    解析发布时间字符串，转换为datetime对象
    例如: "2025-07-19 " -> datetime对象
    """
    try:
        # 去除空格
        time_str = time_str.strip()
        if not time_str:
            return None

        # 尝试解析不同格式
        for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']:
            try:
                return datetime.strptime(time_str, fmt)
            except ValueError:
                continue

        return None
    except Exception as e:
        logger.warning(f"解析时间失败: {time_str}, 错误: {e}")
        return None


def import_video_data():
    """
    从CSV文件导入视频数据到数据库
    :return: 导入记录数
    """
    try:
        if not os.path.exists(VIDEO_CSV_PATH):
            logger.error(f"视频CSV文件不存在: {VIDEO_CSV_PATH}")
            return 0

        logger.info(f"开始导入视频数据: {VIDEO_CSV_PATH}")

        # 读取CSV文件
        df = pd.read_csv(VIDEO_CSV_PATH, encoding='utf-8')

        logger.info(f"CSV文件共 {len(df)} 条数据")

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

        # 数据清洗和转换
        df['publish_time'] = df['publish_time'].apply(parse_publish_time)
        df['duration'] = df['duration'].apply(parse_duration)

        # 填充缺失值
        df['fans_count'] = df['fans_count'].fillna(0)
        df['like_count'] = df['like_count'].fillna(0)
        df['comment_count'] = df['comment_count'].fillna(0)
        df['share_count'] = df['share_count'].fillna(0)
        df['collect_count'] = df['collect_count'].fillna(0)

        count = 0
        for _, row in df.iterrows():
            try:
                # 检查是否已存在
                if VideoData.objects.filter(aweme_id=row['aweme_id']).exists():
                    logger.debug(f"视频已存在，跳过: {row['aweme_id']}")
                    continue

                # 创建Video对象
                VideoData.objects.create(
                    user_name=str(row['user_name']) if pd.notna(row['user_name']) else '',
                    fans_count=int(row['fans_count']),
                    description=str(row['description']) if pd.notna(row['description']) else '',
                    publish_time=row['publish_time'],
                    duration=int(row['duration']),
                    like_count=int(row['like_count']),
                    collect_count=int(row['collect_count']),
                    comment_count=int(row['comment_count']),
                    share_count=int(row['share_count']),
                    aweme_id=str(row['aweme_id'])
                )
                count += 1
                if count % 10 == 0:
                    logger.info(f"已导入 {count} 条视频数据")
            except Exception as e:
                logger.error(f"导入视频数据失败: {row['aweme_id']}, 错误: {e}")
                continue

        logger.info(f"视频数据导入完成，共导入 {count} 条记录")
        return count

    except Exception as e:
        logger.error(f"导入视频数据失败: {e}")
        raise


def import_comment_data():
    """
    从CSV文件导入评论数据到数据库
    :return: 导入记录数
    """
    try:
        if not os.path.exists(COMMENT_CSV_PATH):
            logger.error(f"评论CSV文件不存在: {COMMENT_CSV_PATH}")
            return 0

        logger.info(f"开始导入评论数据: {COMMENT_CSV_PATH}")

        # 读取CSV文件
        df = pd.read_csv(COMMENT_CSV_PATH, encoding='utf-8')

        logger.info(f"CSV文件共 {len(df)} 条数据")

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

        # 数据清洗和转换
        df['comment_time'] = df['comment_time'].apply(parse_publish_time)

        # 填充缺失值
        df['like_count'] = df['like_count'].fillna(0)

        count = 0
        for _, row in df.iterrows():
            try:
                # 创建Comment对象
                CommentData.objects.create(
                    user_id=str(row['user_id']) if pd.notna(row['user_id']) else '',
                    user_name=str(row['user_name']) if pd.notna(row['user_name']) else '',
                    content=str(row['content']) if pd.notna(row['content']) else '',
                    comment_time=row['comment_time'],
                    user_ip=str(row['user_ip']) if pd.notna(row['user_ip']) else '',
                    like_count=int(row['like_count']),
                    aweme_id=str(row['aweme_id']) if pd.notna(row['aweme_id']) else ''
                )
                count += 1
                if count % 50 == 0:
                    logger.info(f"已导入 {count} 条评论数据")
            except Exception as e:
                logger.error(f"导入评论数据失败: {row.get('用户id', '')}, 错误: {e}")
                continue

        logger.info(f"评论数据导入完成，共导入 {count} 条记录")
        return count

    except Exception as e:
        logger.error(f"导入评论数据失败: {e}")
        raise


def import_all_data():
    """
    导入所有CSV数据到数据库
    :return: {'videos': 导入的视频数, 'comments': 导入的评论数}
    """
    logger.info("开始导入所有CSV数据...")

    try:
        video_count = import_video_data()
        comment_count = import_comment_data()

        logger.info(f"所有数据导入完成: 视频 {video_count} 条, 评论 {comment_count} 条")

        return {
            'videos': video_count,
            'comments': comment_count
        }
    except Exception as e:
        logger.error(f"导入所有数据失败: {e}")
        raise