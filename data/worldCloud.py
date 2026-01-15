#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/4 19:38
# @Author  : Rocky

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import matplotlib

from config import Config
import pymysql
conn = pymysql.connect(
    host=Config.DB_HOST,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    db=Config.DB_NAME,
    port=Config.DB_PORT,
    # charset='utf8'
)

cursor = conn.cursor()

matplotlib.use('Tkagg')

# 视频表词云
def video_title_wordCloud():
    sql = "select description from video_data"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for row in data:
        if row[0]:
            text += row[0]

    data_cut = jieba.cut(text, cut_all=False)
    word_text = ' '.join(data_cut)

    wc = WordCloud(
        font_path='simhei.ttf',
        width=800,
        height=600,
        background_color='white',
        max_words=300,
        max_font_size=100,
        min_font_size=10,
        collocations=False,
        prefer_horizontal=0.8
    )
    wc.generate(word_text)
    plt.figure(figsize=(12, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# video_title_wordCloud()

# 评论表词云
def comment_wordCloud():
    sql = "select content from comment_data"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for row in data:
        if row[0]:
            text += row[0]

    data_cut = jieba.cut(text, cut_all=False)
    word_text = ' '.join(data_cut)

    wc = WordCloud(
        font_path='simhei.ttf',
        width=800,
        height=600,
        background_color='white',
        max_words=300,
        max_font_size=100,
        min_font_size=10,
        collocations=False,
        prefer_horizontal=0.8
    )
    wc.generate(word_text)
    plt.figure(figsize=(12, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()