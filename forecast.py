#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/5 20:37
# @Author  : Rocky
import joblib
import pandas as pd

model = joblib.load('build_model/like_model.joblib')
scaler = joblib.load('build_model/like_scaler.joblib')

def predict_like(input_data):
    features = [
        input_data['duration'],
        input_data['collect_count'],
        input_data['comment_count'],
        input_data['share_count'],
        input_data['fans_count'],
        input_data['interact_rate'],
        input_data['publish_hour']
    ]
    features_names = ['视频时长', '收藏数', '评论数', '分享数', '粉丝数量', '互动率', '发布小时']

    df = pd.DataFrame([features], columns=features_names)
    scaler_features = scaler.transform(df)
    prediction = model.predict(scaler_features)
    print(prediction)
    return round(prediction[0], 0)



example_data ={
    'duration': 60,  # 视频时长 1分钟
    'collect_count': 100,   # 收藏数
    'comment_count': 50,    # 评论数
    'share_count': 20,      # 分享数
    'fans_count': 1000,      # 粉丝数量
    'interact_rate': 0.1,    # 互动率
    'publish_hour': 12        # 12点发布
}

print(f'预测结果：{predict_like(example_data)}')
