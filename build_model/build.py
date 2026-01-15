#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/5 16:11
# @Author  : Rocky
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df = pd.read_csv('../data/video_data.csv')

time_column = df.iloc[:, 4]
print(time_column)
seconds = []
for time in time_column:
    minutes, seconds_val = map(int, time.split(':'))
    total_seconds = minutes * 60 + seconds_val
    seconds.append(total_seconds)

df['视频时长'] = seconds

# 特征过程
df['粉丝数量'] = df['粉丝数量'].replace(0, 1)   # 避免除零
df['互动率'] = (df['点赞数'] + df['评论数'] + df['分享数']) / df['粉丝数量']
df['发布时间'] = pd.to_datetime(df['发布时间'])
df['发布小时'] = df['发布时间'].dt.hour

# 选取特征和目标字段
features = df[[
    '视频时长', '收藏数', '评论数', '分享数', '粉丝数量', '互动率', '发布小时'
]]

# 处理异常值
features = features.replace([np.inf, -np.inf], np.nan)
features = features.fillna(features.mean())

target = df['点赞数']

# 数据标准化
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
print(features_scaled)
# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(features_scaled, target, test_size=0.2, random_state=42)

# 创建模型并训练
model = LinearRegression()
model.fit(X_train, y_train)

# 评估模型
y_pred = model.predict(X_test)
print(f'模型R2为: {r2_score(y_test, y_pred): .2f}',)
joblib.dump(model, 'like_model.joblib')
joblib.dump(scaler, 'like_scaler.joblib')

