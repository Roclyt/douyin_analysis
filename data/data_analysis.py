#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/4 20:26
# @Author  : Rocky

import pandas as pd
from config import Config
from sqlalchemy import create_engine

engine = create_engine(f'mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}?charset=utf8')

videdata = pd.read_sql_table('video_data', engine)
commentdata = pd.read_sql_table('comment_data', engine)

# 统计地址
def part1():
    # 统计IP地址
    reslut = commentdata['userIP'].value_counts().reset_index()
    reslut.columns = ['userIP', 'count']
    print(reslut)
    # 写入数据库
    reslut.to_sql('user_ip_Count', engine, if_exists='replace', index=False)

# 统计点赞数，收藏
def part2():
    reslut = videdata[['likeCount', 'collectCount', 'description']] \
        .sort_values('likeCount', ascending=False) \
        .head(10)

    reslut['ratio'] = reslut['collectCount'] / reslut['likeCount']
    print(reslut)
    reslut.to_sql('like_collect_ratio', engine, if_exists='replace', index=False)

# 粉丝数量区间
def part3():
    bins = [-1, 100, 1000, 10000, 100000, float('inf')]
    labels = ['0-99', '100-999', '1000-9999', '10000-99999', '100000+']
    videdata['fansCount'] = pd.cut(videdata['fansCount'], bins=bins, labels=labels)
    reslut = videdata['fansCount'].value_counts().reset_index()
    reslut.columns = ['fansCount', 'count']
    reslut.to_sql('fans_Count', engine, if_exists='replace', index=False)
    print(reslut)

# 粉丝数量排行
def part4():
    videdata_df = videdata[['userName', 'fansCount']]
    result = videdata_df.drop_duplicates('userName')
    result = result.sort_values('fansCount', ascending=False)
    result = result.head(10)
    result.to_sql('fans_rank', engine, if_exists='replace', index=False)
    print(result)


# 评论和分享
def part5():
    videdata_df = videdata[['commentCount', 'shareCount', 'description']]
    result = videdata_df.sort_values('commentCount', ascending=False)
    result = result.head(10)
    result.to_sql('comment_share', engine, if_exists='replace', index=False)

if __name__ == '__main__':
    part1()
    part2()
    part3()
    part4()
    part5()