"""
Django视图和ECharts可视化页面
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import pandas as pd
import numpy as np
import os

from .models import VideoData, CommentData
from data.wordcloud_gen import WordCloudGenerator
from data.ai_analyzer import AIVideoAnalyzer
from data.analyzer import DataAnalyzer

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


def load_video_data_from_csv():
    """
    从CSV文件加载视频数据
    :return: DataFrame
    """
    try:
        if os.path.exists(VIDEO_CSV_PATH):
            df = pd.read_csv(VIDEO_CSV_PATH, encoding='utf-8')

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

            # 数据类型转换
            numeric_columns = ['fans_count', 'like_count', 'collect_count', 'comment_count', 'share_count']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            # 将aweme_id转换为字符串，便于API查找
            if 'aweme_id' in df.columns:
                df['aweme_id'] = df['aweme_id'].astype(str)

            # 解析duration字段
            if 'duration' in df.columns:
                df['duration'] = df['duration'].apply(parse_duration)

            return df
        else:
            logger.warning(f"视频CSV文件不存在: {VIDEO_CSV_PATH}")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"从CSV加载视频数据失败: {e}")
        return pd.DataFrame()


def load_comment_data_from_csv():
    """
    从CSV文件加载评论数据
    :return: DataFrame
    """
    try:
        if os.path.exists(COMMENT_CSV_PATH):
            df = pd.read_csv(COMMENT_CSV_PATH, encoding='utf-8')

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

            # 数据类型转换
            if 'like_count' in df.columns:
                df['like_count'] = pd.to_numeric(df['like_count'], errors='coerce').fillna(0)

            # 将aweme_id转换为字符串，便于筛选
            if 'aweme_id' in df.columns:
                df['aweme_id'] = df['aweme_id'].astype(str)

            return df
        else:
            logger.warning(f"评论CSV文件不存在: {COMMENT_CSV_PATH}")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"从CSV加载评论数据失败: {e}")
        return pd.DataFrame()


def index(request):
    """首页"""
    return render(request, 'index.html')


def dashboard(request):
    """数据仪表盘"""
    analyzer = DataAnalyzer()
    report = analyzer.generate_full_analysis_report()

    return render(request, 'dashboard.html', {
        'report': report
    })


def wordcloud(request):
    """词云分析页面"""
    return render(request, 'wordcloud.html')


def ai_analysis(request):
    """AI分析页面"""
    return render(request, 'ai_analysis.html')


def api_general_stats(request):
    """总体统计数据API"""
    stats = DataAnalyzer.get_general_statistics()
    return JsonResponse({'success': True, 'data': stats})


def api_like_collect_relation(request):
    """点赞收藏关系API"""
    relation = DataAnalyzer.analyze_like_collect_relation()
    return JsonResponse({'success': True, 'data': relation})


def api_fans_distribution(request):
    """粉丝分布API"""
    distribution = DataAnalyzer.categorize_fans_distribution()
    return JsonResponse({'success': True, 'data': distribution})


def api_ip_distribution(request):
    """IP分布API"""
    distribution = DataAnalyzer.analyze_user_ip_distribution()
    return JsonResponse({'success': True, 'data': distribution})


def api_top_users(request):
    """用户排行API"""
    limit = int(request.GET.get('limit', 10))
    users = DataAnalyzer.get_top_users_by_fans(limit=limit)
    return JsonResponse({'success': True, 'data': users})


def api_top_videos(request):
    """视频排行API"""
    limit = int(request.GET.get('limit', 10))
    videos = DataAnalyzer.get_top_videos_by_likes(limit=limit)
    return JsonResponse({'success': True, 'data': videos})


def api_video_statistics(request):
    """视频统计API"""
    stats = DataAnalyzer.analyze_video_statistics()
    return JsonResponse({'success': True, 'data': stats})


def api_publish_time_distribution(request):
    """发布时间分布API"""
    distribution = DataAnalyzer.analyze_publish_time_distribution()
    return JsonResponse({'success': True, 'data': distribution})


def api_full_report(request):
    """完整报告API"""
    report = DataAnalyzer.generate_full_analysis_report()
    return JsonResponse({'success': True, 'data': report})


def api_video_wordcloud(request):
    """视频词云API"""
    try:
        video_id = request.GET.get('video_id')

        generator = WordCloudGenerator()
        result = generator.generate_video_wordcloud(video_id)

        # 将结果包装在data字段中
        if result['success']:
            return JsonResponse({
                'success': True,
                'data': {
                    'image': result['image'],
                    'top_words': result['top_words'],
                    'total_words': result.get('total_words', 0),
                    'video_count': result.get('video_count', 0)
                }
            })
        else:
            return JsonResponse(result)
    except Exception as e:
        logger.error(f"生成视频词云失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


def api_comment_wordcloud(request):
    """评论词云API - 根据视频ID筛选评论生成词云"""
    try:
        video_id = request.GET.get('video_id')

        logger.info(f"生成评论词云，video_id={video_id}")

        generator = WordCloudGenerator()
        result = generator.generate_comment_wordcloud(video_id)

        # 将结果包装在data字段中
        if result['success']:
            return JsonResponse({
                'success': True,
                'data': {
                    'image': result['image'],
                    'keywords': result.get('keywords', []),
                    'total_words': result.get('total_words', 0),
                    'comment_count': result.get('comment_count', 0)
                }
            })
        else:
            # 统一返回error字段，前端期望的是error而不是message
            return JsonResponse({
                'success': False,
                'error': result.get('message', '未知错误')
            })
    except Exception as e:
        logger.error(f"生成评论词云失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


def api_video_keywords(request):
    """视频关键词分析API"""
    try:
        video_id = request.GET.get('video_id')

        if not video_id:
            return JsonResponse({'success': False, 'error': '缺少video_id参数'})

        generator = WordCloudGenerator()
        result = generator.analyze_video_keywords(video_id)

        return JsonResponse(result)
    except Exception as e:
        logger.error(f"分析视频关键词失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def api_analyze_video_url(request):
    """AI分析视频URL API"""
    try:
        video_url = request.POST.get('video_url') or request.GET.get('video_url')

        if not video_url:
            return JsonResponse({'success': False, 'error': '缺少video_url参数'})

        analyzer = AIVideoAnalyzer()
        result = analyzer.analyze_video_url(video_url)

        return JsonResponse(result)
    except Exception as e:
        logger.error(f"AI分析视频失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def api_analyze_video_data(request):
    """AI分析视频数据API"""
    try:
        # 获取video_id，支持JSON POST和GET请求
        if request.method == 'POST':
            # 尝试从JSON body获取
            try:
                import json
                data = json.loads(request.body)
                video_id = data.get('video_id')
            except:
                # 如果JSON解析失败，尝试从POST获取
                video_id = request.POST.get('video_id')
        else:
            video_id = request.GET.get('video_id')

        if not video_id:
            return JsonResponse({'success': False, 'error': '缺少video_id参数'})

        # 从CSV加载视频数据
        df = load_video_data_from_csv()

        if df.empty:
            return JsonResponse({'success': False, 'error': '没有视频数据'})

        video_row = df[df['aweme_id'] == video_id]
        if video_row.empty:
            return JsonResponse({'success': False, 'error': '视频不存在'})

        video = video_row.iloc[0]
        video_data = {
            'aweme_id': str(video['aweme_id']),
            'description': str(video['description']) if pd.notna(video['description']) else '',
            'duration': int(video['duration']),
            'like_count': int(video['like_count']),
            'comment_count': int(video['comment_count']),
            'share_count': int(video['share_count']),
            'collect_count': int(video['collect_count']),
            'view_count': int(video['like_count']) * 10,  # 估算
        }

        analyzer = AIVideoAnalyzer()
        result = analyzer.analyze_video_data(video_data)

        return JsonResponse(result)
    except Exception as e:
        logger.error(f"分析视频数据失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


def api_video_list(request):
    """视频列表API"""
    try:
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))

        # 从CSV加载视频数据
        df = load_video_data_from_csv()

        if df.empty:
            return JsonResponse({
                'success': True,
                'data': {
                    'videos': [],
                    'total': 0
                }
            })

        # 分页
        total = len(df)
        df_page = df.iloc[offset:offset+limit]

        video_list = []
        for _, video in df_page.iterrows():
            description = str(video['description']) if pd.notna(video['description']) else ''
            video_list.append({
                'aweme_id': str(video['aweme_id']),
                'user_name': str(video['user_name']) if pd.notna(video['user_name']) else '',
                'description': description[:100] + '...' if len(description) > 100 else description,
                'publish_time': '',  # CSV中时间格式可能不一致，暂时留空
                'duration': int(video['duration']),
                'like_count': int(video['like_count']),
                'comment_count': int(video['comment_count']),
                'share_count': int(video['share_count']),
                'collect_count': int(video['collect_count']),
                'fans_count': int(video['fans_count'])  # 添加粉丝数字段
            })

        return JsonResponse({
            'success': True,
            'data': {
                'videos': video_list,
                'total': total
            }
        })
    except Exception as e:
        logger.error(f"获取视频列表失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def api_clear_data(request):
    """清空数据API"""
    try:
        from data.storage import DataStorage
        stats = DataStorage.clear_all_data()
        return JsonResponse({'success': True, 'data': stats, 'message': '数据清空成功'})
    except Exception as e:
        logger.error(f"清空数据失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


# 新增页面视图
def video_comments(request):
    """视频评论查看页面"""
    return render(request, 'video_comments.html')


def user_region(request):
    """用户地区分析页面"""
    return render(request, 'user_region.html')


def fans_analysis(request):
    """粉丝数量分析页面"""
    return render(request, 'fans_analysis.html')


def comment_analysis(request):
    """评论分析页面"""
    return render(request, 'comment_analysis.html')


def sentiment_analysis(request):
    """情感分析页面"""
    return render(request, 'sentiment_analysis.html')


def comment_wordcloud(request):
    """评论词云图页面"""
    return render(request, 'comment_wordcloud.html')


# 新增API
def api_video_comments(request):
    """视频评论API - 从CSV文件加载评论数据"""
    try:
        video_id = request.GET.get('video_id', '')
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))

        # 从CSV加载评论数据
        df = load_comment_data_from_csv()

        if df.empty:
            return JsonResponse({
                'success': True,
                'data': {
                    'comments': [],
                    'total': 0
                }
            })

        # 筛选条件：根据视频ID筛选评论
        if video_id:
            df = df[df['aweme_id'] == str(video_id)]
            logger.info(f"筛选视频ID: {video_id}, 找到 {len(df)} 条评论")

        # 分页
        total = len(df)
        offset = (page - 1) * limit
        df_page = df.iloc[offset:offset+limit]

        # 构建评论列表
        comments_list = []
        for _, comment in df_page.iterrows():
            comments_list.append({
                'user_name': str(comment['user_name']) if pd.notna(comment['user_name']) else '',
                'content': str(comment['content']) if pd.notna(comment['content']) else '',
                'like_count': int(comment['like_count']) if pd.notna(comment['like_count']) else 0,
                'user_ip': str(comment['user_ip']) if pd.notna(comment['user_ip']) else '',
                'comment_time': str(comment['comment_time']) if pd.notna(comment['comment_time']) else ''
            })

        return JsonResponse({
            'success': True,
            'data': {
                'comments': comments_list,
                'total': total
            }
        })
    except Exception as e:
        logger.error(f"获取视频评论失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def api_analyze_sentiment(request):
    """分析评论情感API"""
    try:
        from data.sentiment import SentimentAnalyzer

        analyzer = SentimentAnalyzer()
        video_id = request.GET.get('video_id', '')

        if video_id:
            # 按视频ID分析
            result = analyzer.analyze_comments_by_video(video_id)
        else:
            # 分析所有评论
            result = analyzer.analyze_all_comments()

        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        logger.error(f"情感分析失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return JsonResponse({'success': False, 'error': str(e)})


# 点赞数预测相关视图和API
def like_prediction(request):
    """点赞数预测页面"""
    return render(request, 'like_prediction.html')


def api_prediction_stats(request):
    """预测统计数据API"""
    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import train_test_split

        # 从CSV加载数据
        df = load_video_data_from_csv()

        if df.empty or len(df) < 10:
            # 数据不足，返回默认值
            avg_likes = df['like_count'].mean() if not df.empty and 'like_count' in df.columns else 0
            return JsonResponse({
                'success': True,
                'data': {
                    'total_videos': len(df),
                    'accuracy': '数据不足',
                    'avg_likes': int(avg_likes)
                }
            })

        # 准备特征和目标
        videos = df[['comment_count', 'collect_count', 'share_count', 'fans_count', 'duration', 'like_count']].dropna()
        X = videos[['comment_count', 'collect_count', 'share_count', 'fans_count', 'duration']].values
        y = videos['like_count'].values

        # 分割训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 训练模型
        model = LinearRegression()
        model.fit(X_train, y_train)

        # 计算准确率
        train_score = model.score(X_train, y_train) * 100
        test_score = model.score(X_test, y_test) * 100

        avg_likes = int(np.mean(y))

        return JsonResponse({
            'success': True,
            'data': {
                'total_videos': len(videos),
                'accuracy': f"{test_score:.2f}%",
                'avg_likes': avg_likes
            }
        })
    except Exception as e:
        logger.error(f"获取预测统计失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def api_predict_likes(request):
    """预测点赞数API - 返回未来7天预测"""
    try:
        import json
        from sklearn.linear_model import LinearRegression
        from datetime import datetime, timedelta
        import numpy as np

        data = json.loads(request.body)
        video_id = data.get('video_id')

        if not video_id:
            return JsonResponse({'success': False, 'error': '缺少video_id参数'})

        # 从CSV加载数据
        df = load_video_data_from_csv()

        if df.empty or len(df) < 10:
            return JsonResponse({
                'success': False,
                'error': '数据不足，需要至少10条视频数据才能进行预测'
            })

        # 查找指定视频
        video_row = df[df['aweme_id'] == video_id]
        if video_row.empty:
            return JsonResponse({'success': False, 'error': '视频不存在'})

        video = video_row.iloc[0]

        # 准备训练数据
        videos = df[['comment_count', 'collect_count', 'share_count', 'fans_count', 'duration', 'like_count']].dropna()
        X = videos[['comment_count', 'collect_count', 'share_count', 'fans_count', 'duration']].values
        y = videos['like_count'].values

        # 训练模型
        model = LinearRegression()
        model.fit(X, y)

        # 预测当前视频的基础点赞数
        features = [[video['comment_count'], video['collect_count'], video['share_count'],
                   video['fans_count'], video['duration']]]
        base_predicted_likes = model.predict(features)[0]

        # 生成未来7天的预测数据
        # 使用指数增长模型，基于当前互动指标预测未来增长
        current_likes = video['like_count']

        # 计算日均增长率（基于历史数据）
        total_interactions = video['comment_count'] + video['share_count'] + video['collect_count']
        interaction_ratio = total_interactions / max(current_likes, 1)

        # 增长因子：互动越高，增长越快
        growth_factor = 1 + (interaction_ratio * 0.1)

        # 生成未来7天的预测
        future_dates = []
        future_predictions = []

        for day in range(7):
            future_date = datetime.now() + timedelta(days=day + 1)
            future_dates.append(future_date.strftime('%m-%d'))

            # 使用复合增长模型预测
            if day == 0:
                predicted = current_likes
            else:
                # 每天增长逐渐放缓，符合视频传播规律
                daily_growth = (growth_factor - 1) * (0.7 ** day) * current_likes
                predicted = current_likes + sum([daily_growth * (0.9 ** d) for d in range(day + 1)])

            future_predictions.append(int(round(predicted)))

        return JsonResponse({
            'success': True,
            'data': {
                'video_id': video['aweme_id'],
                'description': video['description'],
                'current_likes': int(current_likes),
                'predicted_likes': int(base_predicted_likes),
                'future_dates': future_dates,
                'future_predictions': future_predictions,
                'total_interactions': int(total_interactions)
            }
        })
    except Exception as e:
        logger.error(f"预测点赞数失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


def api_prediction_performance(request):
    """预测模型性能API"""
    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import train_test_split

        # 从CSV加载数据
        df = load_video_data_from_csv()

        if df.empty or len(df) < 10:
            return JsonResponse({
                'success': True,
                'data': {
                    'train_accuracy': 0,
                    'test_accuracy': 0
                }
            })

        # 准备特征和目标
        videos = df[['comment_count', 'collect_count', 'share_count', 'fans_count', 'duration', 'like_count']].dropna()
        X = videos[['comment_count', 'collect_count', 'share_count', 'fans_count', 'duration']].values
        y = videos['like_count'].values

        # 分割训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 训练模型
        model = LinearRegression()
        model.fit(X_train, y_train)

        # 计算准确率
        train_score = model.score(X_train, y_train) * 100
        test_score = model.score(X_test, y_test) * 100

        return JsonResponse({
            'success': True,
            'data': {
                'train_accuracy': round(train_score, 2),
                'test_accuracy': round(test_score, 2)
            }
        })
    except Exception as e:
        logger.error(f"获取预测性能失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


def api_prediction_comparison(request):
    """预测对比数据API"""
    try:
        from sklearn.linear_model import LinearRegression

        # 从CSV加载数据
        df = load_video_data_from_csv()

        if df.empty or len(df) < 10:
            return JsonResponse({
                'success': True,
                'data': {
                    'labels': [],
                    'actual': [],
                    'predicted': []
                }
            })

        # 准备特征和目标
        videos = df[['aweme_id', 'comment_count', 'collect_count', 'share_count', 'fans_count', 'duration', 'like_count']].dropna()
        X = videos[['comment_count', 'collect_count', 'share_count', 'fans_count', 'duration']].values
        y = videos['like_count'].values

        # 训练模型
        model = LinearRegression()
        model.fit(X, y)

        # 预测所有视频
        predicted = model.predict(X)

        # 限制显示前15个
        limit = min(15, len(videos))
        labels = [str(v)[:8] for v in videos['aweme_id'].values[:limit]]
        actual = [int(v) for v in videos['like_count'].values[:limit]]
        predicted = [int(p) for p in predicted[:limit]]

        return JsonResponse({
            'success': True,
            'data': {
                'labels': labels,
                'actual': actual,
                'predicted': predicted
            }
        })
    except Exception as e:
        logger.error(f"获取预测对比数据失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


# AI分析与建议相关视图和API
def ai_suggestions(request):
    """AI分析与建议页面"""
    return render(request, 'ai_suggestions.html')


@csrf_exempt
def api_ai_chat(request):
    """AI对话API"""
    try:
        import json

        data = json.loads(request.body)
        message = data.get('message', '')
        video_id = data.get('video_id', '')

        if not message:
            return JsonResponse({'success': False, 'error': '缺少消息内容'})

        # 如果有视频ID，从CSV获取视频数据作为上下文
        context = None
        if video_id:
            try:
                df = load_video_data_from_csv()
                if not df.empty:
                    video_row = df[df['aweme_id'] == video_id]
                    if not video_row.empty:
                        video = video_row.iloc[0]
                        context = f"""
当前视频数据：
- 视频ID: {video['aweme_id']}
- 用户名: {video['user_name']}
- 粉丝数: {video['fans_count']}
- 视频描述: {video['description']}
- 视频时长: {video['duration']}秒
- 点赞数: {video['like_count']}
- 评论数: {video['comment_count']}
- 分享数: {video['share_count']}
- 收藏数: {video['collect_count']}
"""
            except Exception as e:
                logger.error(f"获取视频数据失败: {e}")
                pass

        # 使用AI分析器
        from data.ai_analyzer import AIVideoAnalyzer

        analyzer = AIVideoAnalyzer()
        result = analyzer.chat(message, context)

        if result['success']:
            return JsonResponse({
                'success': True,
                'data': {
                    'response': result['response']
                }
            })
        else:
            logger.error(f"AI对话失败: {result.get('error')}")
            return JsonResponse({
                'success': False,
                'error': result.get('error', '对话失败')
            })

    except Exception as e:
        logger.error(f"AI对话失败: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def api_ai_analyze_video(request):
    """AI分析视频API"""
    try:
        import json

        data = json.loads(request.body)
        video_id = data.get('video_id')

        if not video_id:
            return JsonResponse({'success': False, 'error': '缺少video_id参数'})

        # 从CSV获取视频数据
        df = load_video_data_from_csv()

        if df.empty:
            return JsonResponse({'success': False, 'error': '没有视频数据'})

        video_row = df[df['aweme_id'] == video_id]
        if video_row.empty:
            return JsonResponse({'success': False, 'error': '视频不存在'})

        video = video_row.iloc[0]

        # 构建视频数据字典
        video_data = {
            'aweme_id': str(video['aweme_id']),
            'user_name': str(video['user_name']) if pd.notna(video['user_name']) else '',
            'fans_count': int(video['fans_count']),
            'description': str(video['description']) if pd.notna(video['description']) else '',
            'publish_time': '',  # CSV中时间格式可能不一致，暂时留空
            'duration': int(video['duration']),
            'like_count': int(video['like_count']),
            'comment_count': int(video['comment_count']),
            'share_count': int(video['share_count']),
            'collect_count': int(video['collect_count']),
        }

        # 使用AI分析器
        from data.ai_analyzer import AIVideoAnalyzer

        analyzer = AIVideoAnalyzer()
        result = analyzer.analyze_video_data(video_data)

        if result['success']:
            return JsonResponse({
                'success': True,
                'data': result['data']
            })
        else:
            logger.error(f"AI分析失败: {result.get('error')}")
            return JsonResponse({
                'success': False,
                'error': result.get('error', '分析失败')
            })

    except Exception as e:
        logger.error(f"AI分析视频失败: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)})


