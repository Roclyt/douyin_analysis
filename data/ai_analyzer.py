#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/14 23:59
# @Author  : Rocky


"""
AI视频分析模块 - 使用OpenAI SDK调用豆包大模型
"""

import logging
import json
from typing import Dict, List
from openai import OpenAI

logger = logging.getLogger(__name__)


class AIVideoAnalyzer:
    """AI视频分析类 - 使用OpenAI SDK调用豆包1.6大模型"""

    def __init__(self):
        # 豆包大模型API配置（使用OpenAI SDK）
        self.api_key = "" #大模型api_key值
        self.base_url = "https://ark.cn-beijing.volces.com/api/v3"
        self.model = ""  #大模型名称
        self.client = None
        self._init_client()

    def _init_client(self):
        """初始化豆包客户端（使用OpenAI SDK）"""
        try:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
            )
            logger.info("豆包大模型客户端初始化成功")
        except Exception as e:
            logger.error(f"豆包大模型客户端初始化失败: {e}")
            self.client = None

    def analyze_video_data(self, video_data: Dict) -> Dict:
        """
        基于视频数据分析并给出建议
        :param video_data: 视频数据字典
        :return: 分析结果
        """
        try:
            if not self.client:
                self._init_client()

            if not self.client:
                return {
                    'success': False,
                    'error': 'AI客户端未初始化，请检查配置'
                }

            # 从视频数据中提取信息
            aweme_id = video_data.get('aweme_id', '')
            user_name = video_data.get('user_name', '')
            fans_count = video_data.get('fans_count', 0)
            description = video_data.get('description', '')
            duration = video_data.get('duration', 0)
            like_count = video_data.get('like_count', 0)
            comment_count = video_data.get('comment_count', 0)
            share_count = video_data.get('share_count', 0)
            collect_count = video_data.get('collect_count', 0)

            # 计算互动率
            view_count = like_count * 10  # 估算播放量
            interaction_rate = (like_count + comment_count + share_count + collect_count) / max(view_count, 1)

            # 计算各项指标率
            like_rate = like_count / max(view_count, 1)
            comment_rate = comment_count / max(view_count, 1)
            share_rate = share_count / max(view_count, 1)
            collect_rate = collect_count / max(view_count, 1)

            # 构建分析提示词
            prompt = f"""请作为专业的抖音内容分析师，对以下视频数据进行深度分析：

【视频基本信息】
- 视频ID: {aweme_id}
- 创作者: {user_name}
- 粉丝数: {fans_count:,}
- 视频描述: {description}
- 视频时长: {duration}秒

【数据表现】
- 点赞数: {like_count:,}
- 评论数: {comment_count:,}
- 分享数: {share_count:,}
- 收藏数: {collect_count:,}
- 互动率: {interaction_rate * 100:.2f}%

请从以下几个方面进行详细分析：

1. **内容定位分析**：
   - 分析视频的主题和风格
   - 识别目标受众群体
   - 评估内容的独特性

2. **数据表现分析**：
   - 分析点赞率({like_rate * 100:.2f}%)、评论率({comment_rate * 100:.2f}%)、分享率({share_rate * 100:.2f}%)、收藏率({collect_rate * 100:.2f}%)
   - 评估各项指标的合理性
   - 识别优势和短板

3. **优化建议**：
   - 标题和描述优化建议（3条）
   - 发布时间建议
   - 内容改进建议（3条）
   - 互动引导建议（3条）

4. **风险评估**：
   - 可能的敏感内容风险
   - 版权风险提示
   - 违规风险

5. **综合评分与建议**：
   - 给出综合评分（0-100分）
   - 总结性建议

请以JSON格式返回分析结果，格式如下：
{{
    "content_positioning": {{
        "theme": "主题",
        "target_audience": "目标受众",
        "uniqueness": "独特性评估"
    }},
    "data_analysis": {{
        "like_rate_comment": "点赞率分析",
        "comment_rate_comment": "评论率分析",
        "share_rate_comment": "分享率分析",
        "collect_rate_comment": "收藏率分析",
        "strengths": ["优势1", "优势2"],
        "weaknesses": ["短板1", "短板2"]
    }},
    "optimization_suggestions": {{
        "title_suggestions": ["建议1", "建议2", "建议3"],
        "publish_time": "发布时间建议",
        "content_improvements": ["改进1", "改进2", "改进3"],
        "interaction_guidance": ["引导1", "引导2", "引导3"]
    }},
    "risk_assessment": {{
        "sensitive_content": "敏感内容风险",
        "copyright_risk": "版权风险",
        "violation_risk": "违规风险"
    }},
    "overall_score": 85,
    "summary": "总结性建议"
}}
"""

            # 调用豆包大模型（使用OpenAI SDK的responses接口）
            logger.info(f"开始分析视频: {aweme_id}")
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )

            # 解析响应 - 豆包API的响应格式
            logger.info(f"豆包大模型响应状态: {response.status}")
            result_text = None

            # 获取output列表
            if hasattr(response, 'output') and response.output:
                # 遍历output列表，找到message类型的内容
                for output_item in response.output:
                    if hasattr(output_item, 'type') and output_item.type == 'message':
                        # 找到message，获取content中的文本
                        if hasattr(output_item, 'content') and output_item.content:
                            for content_item in output_item.content:
                                if hasattr(content_item, 'text'):
                                    result_text = content_item.text
                                    break
                            if result_text:
                                break

            # 如果没有找到，尝试其他格式
            if not result_text:
                # 尝试直接从output[0].content获取
                if response.output and len(response.output) > 0:
                    first_output = response.output[0]
                    if hasattr(first_output, 'content'):
                        if isinstance(first_output.content, list) and len(first_output.content) > 0:
                            first_content = first_output.content[0]
                            if hasattr(first_content, 'text'):
                                result_text = first_content.text
                            else:
                                result_text = str(first_content)
                        else:
                            result_text = str(first_output.content)

            if not result_text:
                raise ValueError("无法从响应中提取文本内容")

            logger.info(f"豆包大模型返回结果长度: {len(result_text)}")

            # 尝试解析JSON
            try:
                # 提取JSON部分（可能包含在```json```标记中）
                json_text = result_text
                if "```json" in result_text:
                    json_start = result_text.find("```json") + 7
                    json_end = result_text.find("```", json_start)
                    json_text = result_text[json_start:json_end].strip()
                elif "```" in result_text:
                    json_start = result_text.find("```") + 3
                    json_end = result_text.find("```", json_start)
                    json_text = result_text[json_start:json_end].strip()

                analysis_result = json.loads(json_text)

                # 添加原始数据到结果中
                analysis_result['metrics'] = {
                    'view_count': view_count,
                    'like_count': like_count,
                    'comment_count': comment_count,
                    'share_count': share_count,
                    'collect_count': collect_count,
                    'interaction_rate': round(interaction_rate * 100, 2),
                    'like_rate': round(like_rate * 100, 2),
                    'comment_rate': round(comment_rate * 100, 2),
                    'share_rate': round(share_rate * 100, 2),
                    'collect_rate': round(collect_rate * 100, 2)
                }

                return {
                    'success': True,
                    'data': analysis_result
                }

            except json.JSONDecodeError as e:
                logger.error(f"解析AI返回的JSON失败: {e}")
                logger.error(f"原始响应: {result_text[:500]}")

                # 如果JSON解析失败，返回原始文本
                return {
                    'success': True,
                    'data': {
                        'raw_response': result_text,
                        'metrics': {
                            'view_count': view_count,
                            'like_count': like_count,
                            'comment_count': comment_count,
                            'share_count': share_count,
                            'collect_count': collect_count,
                            'interaction_rate': round(interaction_rate * 100, 2)
                        }
                    }
                }

        except Exception as e:
            logger.error(f"AI分析视频失败: {e}", exc_info=True)
            return {
                'success': False,
                'error': f'分析失败: {str(e)}'
            }

    def analyze_video_url(self, video_url: str) -> Dict:
        """
        通过视频URL分析视频
        :param video_url: 视频链接
        :return: 分析结果
        """
        try:
            if not self.client:
                self._init_client()

            if not self.client:
                return {
                    'success': False,
                    'error': 'AI客户端未初始化，请检查配置'
                }

            # 构建分析提示
            prompt = f"""请作为专业的抖音内容分析师，对以下视频链接进行分析：

视频链接：{video_url}

由于无法直接访问视频内容，请基于一般性分析框架，给出针对以下方面的分析建议：

1. **内容定位分析**
2. **表现分析**
3. **优化建议**
4. **风险提示**

请以JSON格式返回分析结果。
"""

            # 调用豆包大模型（使用OpenAI SDK的responses接口）
            logger.info(f"开始分析视频URL: {video_url}")
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )

            # 解析响应 - 豆包API的响应格式
            result_text = None

            if hasattr(response, 'output') and response.output:
                for output_item in response.output:
                    if hasattr(output_item, 'type') and output_item.type == 'message':
                        if hasattr(output_item, 'content') and output_item.content:
                            for content_item in output_item.content:
                                if hasattr(content_item, 'text'):
                                    result_text = content_item.text
                                    break
                            if result_text:
                                break

            if not result_text and response.output and len(response.output) > 0:
                first_output = response.output[0]
                if hasattr(first_output, 'content'):
                    if isinstance(first_output.content, list) and len(first_output.content) > 0:
                        first_content = first_output.content[0]
                        if hasattr(first_content, 'text'):
                            result_text = first_content.text
                        else:
                            result_text = str(first_content)
                    else:
                        result_text = str(first_output.content)

            if not result_text:
                raise ValueError("无法从响应中提取文本内容")

            # 尝试解析JSON
            try:
                json_text = result_text
                if "```json" in result_text:
                    json_start = result_text.find("```json") + 7
                    json_end = result_text.find("```", json_start)
                    json_text = result_text[json_start:json_end].strip()

                result = json.loads(json_text)
                result['video_url'] = video_url

                return {
                    'success': True,
                    'data': result
                }

            except json.JSONDecodeError:
                return {
                    'success': True,
                    'data': {
                        'raw_response': result_text,
                        'video_url': video_url
                    }
                }

        except Exception as e:
            logger.error(f"AI分析视频URL失败: {e}", exc_info=True)
            return {
                'success': False,
                'error': f'分析失败: {str(e)}'
            }

    def chat(self, message: str, context: str = None) -> Dict:
        """
        AI对话功能
        :param message: 用户消息
        :param context: 上下文信息（可选）
        :return: 对话结果
        """
        try:
            if not self.client:
                self._init_client()

            if not self.client:
                return {
                    'success': False,
                    'error': 'AI客户端未初始化，请检查配置'
                }

            # 构建提示词
            prompt = f"""你是一个专业的抖音数据分析助手，可以帮助用户分析视频数据、提供内容建议等。

{context if context else '当前没有具体的视频数据上下文。'}

用户问题：{message}

请提供专业、详细、有针对性的回答。
"""

            # 调用豆包大模型（使用OpenAI SDK的responses接口）
            logger.info(f"AI对话，问题: {message[:50]}...")
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )

            # 解析响应 - 豆包API的响应格式
            result_text = None

            if hasattr(response, 'output') and response.output:
                for output_item in response.output:
                    if hasattr(output_item, 'type') and output_item.type == 'message':
                        if hasattr(output_item, 'content') and output_item.content:
                            for content_item in output_item.content:
                                if hasattr(content_item, 'text'):
                                    result_text = content_item.text
                                    break
                            if result_text:
                                break

            if not result_text and response.output and len(response.output) > 0:
                first_output = response.output[0]
                if hasattr(first_output, 'content'):
                    if isinstance(first_output.content, list) and len(first_output.content) > 0:
                        first_content = first_output.content[0]
                        if hasattr(first_content, 'text'):
                            result_text = first_content.text
                        else:
                            result_text = str(first_content)
                    else:
                        result_text = str(first_output.content)

            if not result_text:
                raise ValueError("无法从响应中提取文本内容")

            return {
                'success': True,
                'response': result_text
            }

        except Exception as e:
            logger.error(f"AI对话失败: {e}", exc_info=True)
            return {
                'success': False,
                'error': f'对话失败: {str(e)}'
            }
