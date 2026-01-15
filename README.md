# 抖音数据分析系统

#### 介绍
# 抖音数据分析系统

基于Django框架的抖音视频数据分析系统，提供数据爬取、处理、存储、分析和可视化展示功能。集成AI智能分析能力，支持点赞预测、情感分析、词云生成等多维度分析。

## ✨ 功能特性

### 核心功能

1. **数据管理**
   - 数据爬取：Python爬虫技术爬取抖音视频和评论信息
   - 数据处理：使用Pandas进行数据清洗、去重、去停用词
   - 数据存储：支持MySQL/SQLite数据库存储
   - 数据源：统一使用CSV文件（video_data.csv, comment.csv）

2. **多维度数据分析**
   - 用户IP地域分布分析
   - 点赞与收藏关系分析
   - 用户粉丝数量区间分析
   - 粉丝数排行TOP N
   - 视频排行TOP N
   - 视频发布时间分布

### 高级功能

3. **词云分析** - 可视化展示关键词
   - 视频描述词云生成
   - 评论内容词云生成（支持爱心形状）
   - 高频词汇详细统计
   - 支持按视频ID筛选
   - 图片保存至static文件夹

4. **情感分析** - 基于SnowNLP的评论情感分析
   - 自动识别正面/负面/中性评论
   - 统计情感分布
   - 情感趋势分析

5. **点赞预测** - 机器学习预测视频表现
   - 基于线性回归算法
   - 支持未来7天预测
   - 模型性能评估
   - 预测与实际对比分析

6. **AI智能分析** - 集成豆包大模型
   - 视频内容深度分析
   - AI对话咨询
   - 智能建议生成
   - 视频URL分析

7. **数据可视化** - ECharts展示分析结果
   - 交互式图表
   - 实时数据更新
   - 多种图表类型（柱状图、饼图、折线图、地图等）

8. **后台管理** - SimpleUI美化的Admin后台
   - 视频数据管理
   - 评论数据管理
   - 数据导入导出

## 📊 数据库结构

### VideoData（视频表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键（自增） |
| userName | TEXT | 用户名 |
| fansCount | BIGINT | 粉丝数 |
| description | TEXT | 视频描述 |
| awemeId | TEXT | 视频ID |
| publishTime | DATETIME | 发布时间 |
| duration | TEXT | 视频时长 |
| commentCount | TEXT | 评论数 |
| likeCount | BIGINT | 点赞数 |
| shareCount | BIGINT | 分享数 |
| collectCount | BIGINT | 收藏数 |

### CommentData（评论表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键（自增） |
| userId | TEXT | 用户ID |
| userName | TEXT | 用户名 |
| commentTime | DATETIME | 评论时间 |
| userIP | TEXT | 用户IP |
| content | TEXT | 评论内容 |
| likeCount | BIGINT | 点赞数 |
| awemeId | TEXT | 视频ID（关联VideoData表） |

**注意**：数据库表主要用于存储结构化数据，所有分析功能统一从CSV文件读取数据。

## 🛠 技术栈

### 后端框架
- Django 4.2+（Web框架）
- Django REST（API开发）

### 数据处理与分析
- Pandas 2.0+（数据处理）
- NumPy 1.24+（数值计算）
- Scikit-learn 1.3+（机器学习）
- SnowNLP 0.12+（中文情感分析）
- jieba 0.42+（中文分词）

### 可视化
- ECharts 5.4.3+（图表库）
- WordCloud 1.9.2+（词云生成）
- Matplotlib（图像处理）

### 数据库
- MySQL / SQLite（数据库）
- PyMySQL 1.1+（MySQL驱动）
- SQLAlchemy 2.0+（ORM）

### AI集成
- 豆包大模型（doubao-seed-1-6-251015）

### 其他
- Requests 2.31+（HTTP请求）
- python-dotenv 1.0+（环境变量管理）
- django-simpleui 2024.1+（后台美化）

## 📁 项目结构

```
douyin_analysis/
├── douyin_analysis/          # Django项目配置
│   ├── settings.py           # 项目设置
│   ├── urls.py              # URL路由
│   └── wsgi.py              # WSGI配置
├── video/                   # 视频数据应用
│   ├── models.py            # 数据模型（VideoData, CommentData）
│   ├── views.py             # 视图函数（API接口）
│   ├── urls.py              # 应用URL配置
│   └── admin.py             # 后台管理配置
├── data/                    # 数据处理模块
│   ├── analyzer.py          # 数据分析模块
│   ├── spider.py            # 视频爬取模块
│   ├── spider_comment.py    # 评论爬取模块
│   ├── wordcloud_gen.py     # 词云生成模块（支持爱心形状）
│   ├── sentiment.py         # 情感分析模块
│   ├── storage.py           # 数据存储模块
│   ├── ai_analyzer.py       # AI分析模块（豆包大模型）
│   ├── prediction.py        # 点赞预测模块
│   ├── video_data.csv       # 视频数据CSV文件
│   └── comment.csv          # 评论数据CSV文件
├── templates/               # HTML模板
│   ├── base.html            # 基础模板
│   ├── index.html           # 首页
│   ├── video_comments.html  # 视频评论页面
│   ├── user_region.html     # 用户地域分析
│   ├── fans_analysis.html   # 粉丝分析
│   ├── comment_analysis.html# 评论分析
│   ├── sentiment_analysis.html # 情感分析
│   ├── comment_wordcloud.html # 评论词云
│   ├── like_prediction.html # 点赞预测
│   ├── ai_analysis.html     # AI分析
│   └── ai_suggestions.html  # AI建议
├── static/                  # 静态文件
│   └── *.png               # 生成的词云图片
├── config.py                # 全局配置文件
├── manage.py                # Django管理脚本
├── requirements.txt         # 依赖包列表
├── README.md                # 项目说明

## 暂时没有进行登录注册页面的编写，可自行添加

## 🚀 安装与运行

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+ 或 SQLite 3
- pip 包管理器

### 2. 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd douyin_analysis

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置数据库

编辑 `config.py` 文件：

```python
class Config:
    # 数据库配置
    DB_ENGINE = 'sqlite'  # 或 'mysql'
    DB_NAME = 'dy_analysis'
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'your_password'
    DB_PORT = 3306

    # 字体配置（用于词云）
    FONT_PATH = r'C:\Windows\Fonts\msyh.ttc' #windows自带的字符样式可在C:\Windows\Fonts查找
```

### 4. 数据库迁移

```bash
# 创建数据库表
python manage.py makemigrations video
python manage.py migrate
```

### 5. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

### 6. 运行条件

先将spider_comment.py，spider_video.py单独运行后生成video_data.csv、comment.csv两个文件
运行spider_comment.py，spider_video.py前先将环境补齐，缺失值补全，通过浏览器查看
msToken 和 a_bogus 是抖音 Web 端 / 移动端 API 的核心反爬参数组合，如需批量采集数据需对这两参数加密，可自信处理

**CSV文件格式**：

video_data.csv：
```csv
用户名,粉丝数量,视频描述,发布时间,视频时长,点赞数,收藏数,评论数,分享数,视频ID
```

comment.csv：
```csv
用户id,用户名,评论内容,评论时间,IP地址,点赞数,视频id
```

### 7. 配置AI分析（可选）

如需使用AI分析功能，配置豆包大模型API密钥：

```python
# config.py 或环境变量
DOUBAO_API_KEY = 'your-api-key'
DOUBAO_BASE_URL = 'https://ark.cn-beijing.volces.com/api/v3'
```

### 8. 启动服务器

```bash
python manage.py runserver http://127.0.0.1:8000/
```

### 9. 访问系统

- 首页: http://localhost85000/
- 视频评论: http://localhost:8000/video-comments/
- 用户地域: http://localhost:8000/user-region/
- 粉丝分析: http://localhost:8000/fans-analysis/
- 评论分析: http://localhost:8000/comment-analysis/
- 情感分析: http://localhost:8000/sentiment-analysis/
- 评论词云: http://localhost:8000/comment-wordcloud/
- 点赞预测: http://localhost:8000/like-prediction/
- AI分析: http://localhost:8000/ai-analysis/
- AI建议: http://localhost:8000/ai-suggestions/
- 管理后台: http://localhost:8000/admin/

## 📡 API接口

### 通用统计

- `GET /api/general-stats/` - 总体统计
- `GET /api/like-collect-relation/` - 点赞收藏关系
- `GET /api/fans-distribution/` - 粉丝分布
- `GET /api/ip-distribution/` - IP地域分布
- `GET /api/top-users/?limit=10` - 用户排行
- `GET /api/top-videos/?limit=10` - 视频排行
- `GET /api/video-statistics/` - 视频统计
- `GET /api/publish-time-distribution/` - 发布时间分布
- `GET /api/video-list/?limit=100` - 视频列表
- `GET /api/full-report/` - 完整分析报告

### 评论分析

- `GET /api/video-comments/?aweme_id=xxx` - 获取指定视频的评论
- `GET /api/analyze-sentiment/?aweme_id=xxx` - 情感分析

### 词云分析

- `GET /api/video-wordcloud/?video_id=xxx` - 视频词云
- `GET /api/comment-wordcloud/?video_id=xxx` - 评论词云（支持爱心形状）
- `GET /api/video-keywords/?video_id=xxx` - 视频关键词

### 点赞预测

- `GET /api/prediction-stats/` - 预测统计
- `GET /api/predict-likes/?aweme_id=xxx` - 点赞预测（未来7天）
- `GET /api/prediction-performance/` - 模型性能评估
- `GET /api/prediction-comparison/` - 预测对比

### AI分析

- `POST /api/analyze-video-url/` - 分析视频URL
- `POST /api/analyze-video-data/` - 分析视频数据
- `POST /api/ai-chat/` - AI对话
- `POST /api/ai-analyze-video/` - AI视频分析

### 数据管理

- `POST /api/clear-data/` - 清空数据

## 🔧 配置说明

### 字体配置

词云生成需要中文字体支持，配置 `config.py`：

```python
class Config:
    FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    # 或系统其他中文字体路径
```

### 数据库配置

支持MySQL和SQLite：

```python
# MySQL
class Config:
    DB_ENGINE = 'mysql'
    DB_NAME = 'dy_analysis'
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'password'
    DB_PORT = 3306

# SQLite
class Config:
    DB_ENGINE = 'sqlite'
    DB_NAME = 'db.sqlite3'
```

## ⚠️ 已知问题

### 1. 评论词云生成失败
**问题**：部分视频无评论数据时，页面提示"生成词云失败: undefined"

**原因**：API返回错误时使用`message`字段，前端期望`error`字段

**解决**：已修复，统一使用`error`字段返回错误信息

### 2. AI分析模块报错
**问题**：`No module named 'data.llm_client'`

**解决**：已重构为`data.ai_analyzer`，使用OpenAI SDK调用豆包大模型

### 3. 点赞预测网络错误
**问题**：前端报"网络错误"但API返回200

**原因**：图表实例管理不当

**解决**：优化了图表实例的dispose和init逻辑

详细问题和解决方案请查看 [PROJECT_REPORT.md](PROJECT_REPORT.md)


### 主要模块图片
![首页](%E9%A6%96%E9%A1%B5.JPG)
![用户地区分析](%E7%94%A8%E6%88%B7%E5%9C%B0%E5%8C%BA%E7%BB%9F%E8%AE%A1.JPG)
![词云图](%E8%AF%8D%E4%BA%91%E5%9B%BE%E7%94%9F%E6%88%90%E6%A8%A1%E5%9D%971.JPG)
![情感分析](%E6%83%85%E6%84%9F%E5%88%86%E6%9E%90.JPG)
![AI短视频分析](AI%E8%A7%86%E9%A2%91%E5%88%86%E6%9E%90%E5%92%8C%E5%BB%BA%E8%AE%AE.JPG)
![点赞预测模块1](%E7%82%B9%E8%B5%9E%E9%A2%84%E6%B5%8B%E6%A8%A1%E5%9D%971.JPG)
![点赞预测模块2](%E7%82%B9%E8%B5%9E%E9%A2%84%E6%B5%8B%E6%A8%A1%E5%9D%972.JPG)
![粉丝数量模块1](%E7%B2%89%E4%B8%9D%E6%95%B0%E9%87%8F%E6%A8%A1%E5%9D%971.JPG)
![粉丝数量模块2](%E7%B2%89%E4%B8%9D%E6%95%B0%E9%87%8F%E6%A8%A1%E5%9D%972.JPG)
![评论分析模块1](%E8%AF%84%E8%AE%BA%E5%88%86%E6%9E%90%E6%A8%A1%E5%9D%97.JPG)
![评论分析模块2](%E8%AF%84%E8%AE%BA%E5%88%86%E6%9E%90%E6%A8%A1%E5%9D%972.JPG)


## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

如有问题，请提交Issue。
wx18043401047

有老板在招聘爬虫、数分、RPA的请联系俺，25届还在努力找工作的小菜鸡o(╥﹏╥)oo(╥﹏╥)oo(╥﹏╥)o😭😭😭
