#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/3 10:38
# @Author  : Rocky

"""
Django项目配置文件
用于数据库配置和词云配置
"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent


class Config:
    """项目配置类"""

    # ==================== 数据库配置 ====================
    DB_ENGINE = 'mysql'
    DB_HOST = 'localhost'
    DB_NAME = 'dy_analysis'
    DB_USER = 'root'
    DB_PASSWORD = '123456'
    DB_PORT = 3306

    # 词云配置
    WORDCLOUD_FONT_PATH = r'C:\Windows\Fonts\msyh.ttc'

    @classmethod
    def get_database_url(cls):
        """获取数据库连接URL"""
        # if cls.DB_ENGINE == 'sqlite3':
        #     return f'sqlite:///{cls.DB_NAME}'
        if cls.DB_ENGINE == 'mysql':
            return f'mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}?charset=utf8mb4'
        else:
            raise ValueError(f"不支持的数据库引擎: {cls.DB_ENGINE}")

    @classmethod
    def get_django_db_config(cls):
        """获取Django数据库配置字典"""
        if cls.DB_ENGINE == 'mysql':
            return {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': cls.DB_NAME,
                'USER': cls.DB_USER,
                'PASSWORD': cls.DB_PASSWORD,
                'HOST': cls.DB_HOST,
                'PORT': str(cls.DB_PORT),
                'OPTIONS': {
                    'charset': 'utf8mb4',
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                },
            }
        elif cls.DB_ENGINE == 'sqlite3':
            return {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        else:
            raise ValueError(f"不支持的数据库引擎: {cls.DB_ENGINE}")


# ==================== 辅助函数 ====================
def get_font_path():
    """
    获取可用的中文字体路径

    Returns:
        str: 可用的字体路径，如果没有找到则返回默认路径
    """
    if os.path.exists(Config.WORDCLOUD_FONT_PATH):
        return Config.WORDCLOUD_FONT_PATH

    # 备用字体路径
    backup_fonts = [
        '/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc',
        r'C:/Windows/Fonts/STHUPO.ttf',
        r'C:/Windows/Fonts/simsun.ttc',
    ]

    for font_path in backup_fonts:
        if os.path.exists(font_path):
            return font_path

    return Config.WORDCLOUD_FONT_PATH


if __name__ == '__main__':
    # 测试配置
    print("=" * 50)
    print("配置信息")
    print("=" * 50)
    print(f"数据库引擎: {Config.DB_ENGINE}")
    print(f"数据库主机: {Config.DB_HOST}")
    print(f"数据库名称: {Config.DB_NAME}")
    print(f"数据库用户: {Config.DB_USER}")
    print(f"数据库端口: {Config.DB_PORT}")
    print(f"词云字体: {get_font_path()}")
    print(f"数据库URL: {Config.get_database_url()}")
