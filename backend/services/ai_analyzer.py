import openai
import pandas as pd
import json
import logging
from typing import List, Dict, Any
import asyncio
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """AI分析器，使用DeepSeek模型进行图表推荐"""
    
    def __init__(self):
        # DeepSeek API配置
        self.api_key = "sk-51852758f38143c89493c6568d046330"
        self.model = "deepseek-chat"
        self.base_url = "https://api.deepseek.com"
        
        # 初始化OpenAI客户端（兼容DeepSeek API）
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # 图表类型定义
        self.chart_types = [
            {"name": "条形图", "description": "用水平或垂直条显示不同类别的数值比较", "suitable": "分类数据，数量型数据"},
            {"name": "柱状图", "description": "类似条形图，但条为竖直方向", "suitable": "分类数据，数量型数据"},
            {"name": "折线图", "description": "用线段连接各数据点，显示随时间变化的趋势", "suitable": "序列数据，时间序列数据"},
            {"name": "饼图", "description": "显示各部分占整体的比例", "suitable": "分类数据，比例数据"},
            {"name": "散点图", "description": "展示两个变量之间的关系或相关性", "suitable": "数值型数据，连续数据"},
            {"name": "面积图", "description": "类似折线图，线下部分填充颜色，显示数量变化和累计趋势", "suitable": "序列数据，时间序列数据"},
            {"name": "雷达图", "description": "多维数据呈放射状，比较多项指标", "suitable": "多变量数据"},
            {"name": "箱线图", "description": "展示数据的分布、异常值、中位数、四分位数", "suitable": "数值型数据"},
            {"name": "直方图", "description": "显示数据分布的频数，分组显示", "suitable": "连续数值型数据"},
            {"name": "热力图", "description": "用颜色强度表示数值大小", "suitable": "矩阵型数据，多变量数据"},
            {"name": "瀑布图", "description": "显示累加或减的过程和每步的影响", "suitable": "累计数据"},
            {"name": "漏斗图", "description": "展示流程各阶段的转化量", "suitable": "分阶段数据，流程数据"},
            {"name": "树形图", "description": "用嵌套矩形表示层级及比例", "suitable": "层级数据，比例数据"},
            {"name": "泡泡图", "description": "类似散点图，但点的大小也代表一个变量", "suitable": "多变量数值型数据"},
            {"name": "桑基图", "description": "显示能量、资金等流动的路径和数量", "suitable": "流程数据，流量数据"},
            {"name": "玫瑰图", "description": "类似极坐标下的条形图，显示各类的频数或大小", "suitable": "分类数据，时间周期数据"},
            {"name": "堆积条形图", "description": "条形图变体，分类内部再按子类堆叠", "suitable": "分类数据，子分类数据"},
            {"name": "堆积面积图", "description": "面积图变体，多组数据堆叠显示", "suitable": "时间序列，多组数据"},
            {"name": "双轴图", "description": "用两个坐标轴展示两组相关但量纲不同的数据", "suitable": "多变量时间序列数据"}
        ]
    
    async def recommend_charts(self, df: pd.DataFrame, columns_info: List[Dict]) -> List[Dict]:
        """
        基于数据特征推荐图表类型
        
        Args:
            df: 清洗后的数据
            columns_info: 列信息
            
        Returns:
            图表推荐列表
        """
        try:
            # 准备数据摘要
            data_summary = self._prepare_data_summary(df, columns_info)
            
            # 构造AI提示词
            prompt = self._build_chart_recommendation_prompt(data_summary)
            
            # 调用DeepSeek API
            recommendations = await self._call_deepseek_api(prompt)
            
            # 验证和标准化推荐结果
            validated_recommendations = self._validate_recommendations(recommendations)
            
            logger.info(f"AI推荐完成，返回{len(validated_recommendations)}个图表类型")
            return validated_recommendations
            
        except Exception as e:
            logger.error(f"AI图表推荐失败: {str(e)}")
            # 返回默认推荐
            return self._get_default_recommendations(columns_info)
    
    def _prepare_data_summary(self, df: pd.DataFrame, columns_info: List[Dict]) -> Dict:
        """准备数据摘要"""
        return {
            "row_count": len(df),
            "column_count": len(columns_info),
            "columns": columns_info,
            "data_sample": df.head(5).to_dict('records') if len(df) > 0 else [],
            "data_types": {
                "numeric_columns": [col["name"] for col in columns_info if col["type"] == "number"],
                "date_columns": [col["name"] for col in columns_info if col["type"] == "date"],
                "string_columns": [col["name"] for col in columns_info if col["type"] == "string"],
                "boolean_columns": [col["name"] for col in columns_info if col["type"] == "boolean"]
            }
        }
    
    def _build_chart_recommendation_prompt(self, data_summary: Dict) -> str:
        """构建图表推荐的AI提示词"""
        
        chart_types_text = "\n".join([
            f"{i+1}. {chart['name']}: {chart['description']} (适用于: {chart['suitable']})"
            for i, chart in enumerate(self.chart_types)
        ])
        
        prompt = f"""
你是一名专业的数据分析师，请根据以下数据特征，从30种图表中推荐最适合的3种图表类型。

数据摘要：
- 总行数: {data_summary['row_count']}
- 总列数: {data_summary['column_count']}
- 数值列: {data_summary['data_types']['numeric_columns']}
- 日期列: {data_summary['data_types']['date_columns']}  
- 文本列: {data_summary['data_types']['string_columns']}
- 布尔列: {data_summary['data_types']['boolean_columns']}

列详细信息:
{json.dumps(data_summary['columns'], ensure_ascii=False, indent=2)}

数据样本 (前5行):
{json.dumps(data_summary['data_sample'], ensure_ascii=False, indent=2)}

可选图表类型:
{chart_types_text}

请分析数据特征，考虑以下因素：
1. 数据类型组合（数值、日期、分类等）
2. 数据量级和分布
3. 变量间的关系
4. 可视化的目标和用途

返回JSON格式结果，包含推荐的3种图表，按推荐度排序：
[
  {{"chart":"图表名称","reason":"推荐理由","score":0.95}},
  {{"chart":"图表名称","reason":"推荐理由","score":0.88}},
  {{"chart":"图表名称","reason":"推荐理由","score":0.82}}
]

要求：
- score为0-1之间的小数，表示推荐置信度
- reason要简洁明了，说明为什么适合这种图表
- 优先推荐最能体现数据特征和关系的图表类型
"""
        
        return prompt
    
    async def _call_deepseek_api(self, prompt: str) -> List[Dict]:
        """调用DeepSeek API"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "你是一名专业的数据可视化专家，具有丰富的图表设计经验。请根据用户提供的数据特征，推荐最合适的图表类型。"
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.1,  # 低温度保证结果稳定
                max_tokens=1500,
                top_p=0.9
            )
            
            content = response.choices[0].message.content
            logger.info(f"DeepSeek API响应: {content}")
            
            # 解析JSON响应
            try:
                # 提取JSON部分
                json_start = content.find('[')
                json_end = content.rfind(']') + 1
                json_str = content[json_start:json_end]
                
                recommendations = json.loads(json_str)
                return recommendations
                
            except json.JSONDecodeError as e:
                logger.error(f"解析AI响应JSON失败: {str(e)}")
                logger.error(f"原始响应: {content}")
                raise
                
        except Exception as e:
            logger.error(f"调用DeepSeek API失败: {str(e)}")
            raise
    
    def _validate_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """验证和标准化推荐结果"""
        validated = []
        
        valid_chart_names = {chart["name"] for chart in self.chart_types}
        
        for rec in recommendations:
            # 检查必需字段
            if not all(key in rec for key in ["chart", "reason", "score"]):
                continue
                
            # 验证图表名称
            if rec["chart"] not in valid_chart_names:
                # 尝试模糊匹配
                matched_chart = self._fuzzy_match_chart(rec["chart"])
                if matched_chart:
                    rec["chart"] = matched_chart
                else:
                    continue
            
            # 验证分数范围
            score = float(rec["score"])
            if not (0 <= score <= 1):
                score = max(0, min(1, score))  # 限制在0-1范围内
                rec["score"] = score
            
            validated.append(rec)
        
        # 确保至少有3个推荐
        while len(validated) < 3:
            default_charts = ["柱状图", "折线图", "饼图"]
            for chart in default_charts:
                if chart not in [r["chart"] for r in validated]:
                    validated.append({
                        "chart": chart,
                        "reason": "默认推荐",
                        "score": 0.6
                    })
                    break
        
        # 按分数排序并取前3个
        validated.sort(key=lambda x: x["score"], reverse=True)
        return validated[:3]
    
    def _fuzzy_match_chart(self, chart_name: str) -> str:
        """模糊匹配图表名称"""
        valid_names = [chart["name"] for chart in self.chart_types]
        
        # 简单的字符串相似度匹配
        for valid_name in valid_names:
            if chart_name in valid_name or valid_name in chart_name:
                return valid_name
        
        return None
    
    def _get_default_recommendations(self, columns_info: List[Dict]) -> List[Dict]:
        """获取默认推荐（当AI调用失败时使用）"""
        numeric_cols = [col for col in columns_info if col["type"] == "number"]
        date_cols = [col for col in columns_info if col["type"] == "date"]
        string_cols = [col for col in columns_info if col["type"] == "string"]
        
        recommendations = []
        
        # 基于数据类型的简单规则推荐
        if len(date_cols) > 0 and len(numeric_cols) > 0:
            recommendations.append({
                "chart": "折线图",
                "reason": "包含时间序列和数值数据，适合显示趋势",
                "score": 0.9
            })
        
        if len(string_cols) > 0 and len(numeric_cols) > 0:
            recommendations.append({
                "chart": "柱状图", 
                "reason": "包含分类和数值数据，适合对比分析",
                "score": 0.85
            })
        
        if len(numeric_cols) >= 2:
            recommendations.append({
                "chart": "散点图",
                "reason": "包含多个数值变量，适合分析相关性",
                "score": 0.8
            })
        
        # 补充默认推荐
        default_charts = [
            {"chart": "饼图", "reason": "通用比例展示", "score": 0.7},
            {"chart": "面积图", "reason": "数据趋势可视化", "score": 0.65},
            {"chart": "雷达图", "reason": "多维度数据对比", "score": 0.6}
        ]
        
        for default in default_charts:
            if len(recommendations) >= 3:
                break
            if default["chart"] not in [r["chart"] for r in recommendations]:
                recommendations.append(default)
        
        return recommendations[:3]