#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/4 21:06
# @Author  : Rocky

import pandas as pd
import jieba
from snownlp import SnowNLP

def nlpdemo(df):
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        # stopwords = [line.strip() for line in f.readlines()]
        stopwords = [line.strip() for line in f]

    # 存储结果
    scors = []
    # 分词结果
    segmented_comments = []

    for comment in df['评论内容']:
        comment = str(comment)

        words = jieba.cut(comment)
        filter_words = [word for word in words if word not in stopwords]
        filter_text = ' '.join(filter_words)
        segmented_comments.append(' '.join(filter_words))
        if not filter_text.strip():
            scors.append(0.5)
        else:
            s = SnowNLP(filter_text)
            scors.append(s.sentiments)
    df['scores'] = scors
    df['segmented'] = segmented_comments

    df.to_csv('nlp_result.csv', index=False, encoding='utf-8')




if __name__ == '__main__':
    df = pd.read_csv('comment.csv')
    nlpdemo(df)

