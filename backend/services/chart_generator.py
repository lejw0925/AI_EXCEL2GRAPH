import logging
from typing import Dict, List, Any
import json

logger = logging.getLogger(__name__)

class ChartGenerator:
    """图表配置生成器"""
    
    def __init__(self):
        # 颜色主题
        self.color_themes = [
            ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
            ['#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d3'],
            ['#d62728', '#ff9896', '#2ca02c', '#98df8a', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d3'],
            ['#9467bd', '#c5b0d5', '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896'],
            ['#ff7f0e', '#ffbb78', '#d62728', '#ff9896', '#2ca02c', '#98df8a', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94'],
            ['#17becf', '#9edae5', '#1f77b4', '#aec7e8', '#2ca02c', '#98df8a', '#ff7f0e', '#ffbb78', '#d62728', '#ff9896']
        ]
        
        # 支持的图表类型
        self.supported_charts = [
            "条形图", "柱状图", "折线图", "饼图", "散点图", "面积图", "雷达图", "箱线图", 
            "直方图", "热力图", "瀑布图", "漏斗图", "树形图", "泡泡图", "桑基图", 
            "玫瑰图", "堆积条形图", "堆积面积图", "双轴图"
        ]
    
    def generate_config(self, chart_type: str, data: List[Dict], columns: List[Dict], custom_config: Dict = None) -> Dict:
        """
        生成ECharts图表配置
        
        Args:
            chart_type: 图表类型
            data: 数据
            columns: 列信息
            custom_config: 自定义配置
            
        Returns:
            ECharts配置对象
        """
        try:
            if custom_config is None:
                custom_config = {}
                
            # 获取颜色主题
            colors = self.color_themes[custom_config.get('colorTheme', 0)]
            
            # 基础配置
            base_config = {
                'backgroundColor': 'transparent',
                'color': colors,
                'title': {
                    'text': custom_config.get('title', ''),
                    'left': 'center',
                    'textStyle': {
                        'fontSize': 16,
                        'fontWeight': 'bold'
                    }
                },
                'tooltip': {
                    'trigger': 'axis',
                    'axisPointer': {
                        'type': 'shadow'
                    }
                },
                'legend': {
                    'show': custom_config.get('legendPosition', 'top') != 'none',
                    'orient': 'vertical' if custom_config.get('legendPosition') in ['left', 'right'] else 'horizontal',
                    'left': self._get_legend_position(custom_config.get('legendPosition', 'top'), 'left'),
                    'top': self._get_legend_position(custom_config.get('legendPosition', 'top'), 'top')
                },
                'grid': {
                    'show': custom_config.get('showGrid', True),
                    'left': '3%',
                    'right': '4%', 
                    'bottom': '3%',
                    'containLabel': True
                }
            }
            
            # 根据图表类型生成具体配置
            if chart_type in ['条形图', '柱状图']:
                config = self._generate_bar_chart(data, columns, base_config, chart_type == '条形图')
            elif chart_type == '折线图':
                config = self._generate_line_chart(data, columns, base_config)
            elif chart_type == '饼图':
                config = self._generate_pie_chart(data, columns, base_config)
            elif chart_type == '散点图':
                config = self._generate_scatter_chart(data, columns, base_config)
            elif chart_type == '面积图':
                config = self._generate_area_chart(data, columns, base_config)
            elif chart_type == '雷达图':
                config = self._generate_radar_chart(data, columns, base_config)
            elif chart_type == '热力图':
                config = self._generate_heatmap_chart(data, columns, base_config)
            elif chart_type == '漏斗图':
                config = self._generate_funnel_chart(data, columns, base_config)
            elif chart_type == '堆积条形图':
                config = self._generate_stacked_bar_chart(data, columns, base_config)
            elif chart_type == '堆积面积图':
                config = self._generate_stacked_area_chart(data, columns, base_config)
            else:
                # 默认生成柱状图
                config = self._generate_bar_chart(data, columns, base_config, False)
            
            logger.info(f"生成{chart_type}配置成功")
            return config
            
        except Exception as e:
            logger.error(f"生成图表配置失败: {str(e)}")
            raise
    
    def _get_legend_position(self, position: str, axis: str) -> str:
        """获取图例位置"""
        position_map = {
            'top': {'left': 'center', 'top': 'top'},
            'bottom': {'left': 'center', 'top': 'bottom'},
            'left': {'left': 'left', 'top': 'middle'},
            'right': {'left': 'right', 'top': 'middle'}
        }
        return position_map.get(position, position_map['top'])[axis]
    
    def _find_column_by_type(self, columns: List[Dict], data_type: str) -> Dict:
        """根据类型查找列"""
        for col in columns:
            if col.get('type') == data_type:
                return col
        return columns[0] if columns else {'name': 'default', 'type': 'string'}
    
    def _generate_bar_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict, is_horizontal: bool = False) -> Dict:
        """生成条形图/柱状图配置"""
        category_col = self._find_column_by_type(columns, 'string')
        value_col = self._find_column_by_type(columns, 'number')
        
        categories = [row.get(category_col['name'], '') for row in data]
        values = [row.get(value_col['name'], 0) for row in data]
        
        config = base_config.copy()
        config.update({
            'xAxis': {
                'type': 'value' if is_horizontal else 'category',
                'data': None if is_horizontal else categories,
                'axisTick': {'alignWithLabel': True}
            },
            'yAxis': {
                'type': 'category' if is_horizontal else 'value',
                'data': categories if is_horizontal else None
            },
            'series': [{
                'name': value_col['name'],
                'type': 'bar',
                'data': values,
                'emphasis': {'focus': 'series'}
            }]
        })
        
        return config
    
    def _generate_line_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict) -> Dict:
        """生成折线图配置"""
        x_col = self._find_column_by_type(columns, 'date')
        if x_col['type'] != 'date':
            x_col = self._find_column_by_type(columns, 'string')
        y_col = self._find_column_by_type(columns, 'number')
        
        x_data = [row.get(x_col['name'], '') for row in data]
        y_data = [row.get(y_col['name'], 0) for row in data]
        
        config = base_config.copy()
        config.update({
            'xAxis': {
                'type': 'category',
                'data': x_data,
                'boundaryGap': False
            },
            'yAxis': {
                'type': 'value'
            },
            'series': [{
                'name': y_col['name'],
                'type': 'line',
                'data': y_data,
                'smooth': True,
                'emphasis': {'focus': 'series'}
            }]
        })
        
        return config
    
    def _generate_pie_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict) -> Dict:
        """生成饼图配置"""
        name_col = self._find_column_by_type(columns, 'string')
        value_col = self._find_column_by_type(columns, 'number')
        
        pie_data = [
            {
                'name': row.get(name_col['name'], ''),
                'value': row.get(value_col['name'], 0)
            }
            for row in data
        ]
        
        config = base_config.copy()
        config.update({
            'tooltip': {
                'trigger': 'item',
                'formatter': '{a} <br/>{b}: {c} ({d}%)'
            },
            'series': [{
                'name': name_col['name'],
                'type': 'pie',
                'radius': '50%',
                'data': pie_data,
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        })
        
        # 删除不适用的配置
        config.pop('xAxis', None)
        config.pop('yAxis', None)
        config.pop('grid', None)
        
        return config
    
    def _generate_scatter_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict) -> Dict:
        """生成散点图配置"""
        numeric_cols = [col for col in columns if col.get('type') == 'number']
        if len(numeric_cols) < 2:
            return self._generate_bar_chart(data, columns, base_config)
        
        x_col = numeric_cols[0]
        y_col = numeric_cols[1]
        
        scatter_data = [
            [row.get(x_col['name'], 0), row.get(y_col['name'], 0)]
            for row in data
        ]
        
        config = base_config.copy()
        config.update({
            'xAxis': {
                'type': 'value',
                'name': x_col['name'],
                'nameLocation': 'middle',
                'nameGap': 30
            },
            'yAxis': {
                'type': 'value',
                'name': y_col['name'],
                'nameLocation': 'middle',
                'nameGap': 50
            },
            'series': [{
                'name': f"{x_col['name']} vs {y_col['name']}",
                'type': 'scatter',
                'data': scatter_data,
                'symbolSize': 8,
                'emphasis': {'focus': 'series'}
            }]
        })
        
        return config
    
    def _generate_area_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict) -> Dict:
        """生成面积图配置"""
        config = self._generate_line_chart(data, columns, base_config)
        
        # 为系列添加面积样式
        config['series'][0]['areaStyle'] = {'opacity': 0.6}
        
        return config
    
    def _generate_radar_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict) -> Dict:
        """生成雷达图配置"""
        numeric_cols = [col for col in columns if col.get('type') == 'number']
        
        if len(numeric_cols) < 3:
            return self._generate_bar_chart(data, columns, base_config)
        
        # 计算每个指标的最大值
        indicators = []
        for col in numeric_cols:
            values = [row.get(col['name'], 0) for row in data if row.get(col['name']) is not None]
            max_val = max(values) if values else 100
            indicators.append({
                'name': col['name'],
                'max': max_val * 1.2
            })
        
        # 生成雷达数据
        radar_data = []
        for i, row in enumerate(data[:5]):  # 限制显示前5行
            values = [row.get(col['name'], 0) for col in numeric_cols]
            radar_data.append({
                'value': values,
                'name': f'数据{i+1}'
            })
        
        config = base_config.copy()
        config.update({
            'radar': {
                'indicator': indicators
            },
            'series': [{
                'name': '雷达图',
                'type': 'radar',
                'data': radar_data
            }]
        })
        
        # 删除不适用的配置
        config.pop('xAxis', None)
        config.pop('yAxis', None)
        config.pop('grid', None)
        
        return config
    
    def _generate_heatmap_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict) -> Dict:
        """生成热力图配置"""
        if len(columns) < 3:
            return self._generate_bar_chart(data, columns, base_config)
        
        x_col = columns[0]
        y_col = columns[1]
        value_col = self._find_column_by_type(columns, 'number')
        
        # 获取唯一的x和y值
        x_values = list(set(row.get(x_col['name'], '') for row in data))
        y_values = list(set(row.get(y_col['name'], '') for row in data))
        
        # 生成热力图数据
        heatmap_data = []
        for i, x_val in enumerate(x_values):
            for j, y_val in enumerate(y_values):
                # 查找对应的值
                value = 0
                for row in data:
                    if row.get(x_col['name']) == x_val and row.get(y_col['name']) == y_val:
                        value = row.get(value_col['name'], 0)
                        break
                heatmap_data.append([i, j, value])
        
        values = [item[2] for item in heatmap_data]
        min_val = min(values) if values else 0
        max_val = max(values) if values else 100
        
        config = base_config.copy()
        config.update({
            'xAxis': {
                'type': 'category',
                'data': x_values
            },
            'yAxis': {
                'type': 'category',
                'data': y_values
            },
            'visualMap': {
                'min': min_val,
                'max': max_val,
                'calculable': True,
                'orient': 'horizontal',
                'left': 'center',
                'bottom': '15%'
            },
            'series': [{
                'name': value_col['name'],
                'type': 'heatmap',
                'data': heatmap_data,
                'label': {'show': True},
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        })
        
        return config
    
    def _generate_funnel_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict) -> Dict:
        """生成漏斗图配置"""
        name_col = self._find_column_by_type(columns, 'string')
        value_col = self._find_column_by_type(columns, 'number')
        
        funnel_data = [
            {
                'name': row.get(name_col['name'], ''),
                'value': row.get(value_col['name'], 0)
            }
            for row in data
        ]
        
        # 按值排序
        funnel_data.sort(key=lambda x: x['value'], reverse=True)
        
        config = base_config.copy()
        config.update({
            'tooltip': {
                'trigger': 'item',
                'formatter': '{a} <br/>{b}: {c} ({d}%)'
            },
            'series': [{
                'name': name_col['name'],
                'type': 'funnel',
                'left': '10%',
                'top': 60,
                'bottom': 60,
                'width': '80%',
                'data': funnel_data
            }]
        })
        
        # 删除不适用的配置
        config.pop('xAxis', None)
        config.pop('yAxis', None)
        config.pop('grid', None)
        
        return config
    
    def _generate_stacked_bar_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict) -> Dict:
        """生成堆积条形图配置"""
        category_col = self._find_column_by_type(columns, 'string')
        numeric_cols = [col for col in columns if col.get('type') == 'number']
        
        if len(numeric_cols) < 2:
            return self._generate_bar_chart(data, columns, base_config)
        
        categories = list(set(row.get(category_col['name'], '') for row in data))
        
        series = []
        for col in numeric_cols:
            col_data = []
            for cat in categories:
                value = 0
                for row in data:
                    if row.get(category_col['name']) == cat:
                        value = row.get(col['name'], 0)
                        break
                col_data.append(value)
            
            series.append({
                'name': col['name'],
                'type': 'bar',
                'stack': 'total',
                'data': col_data
            })
        
        config = base_config.copy()
        config.update({
            'xAxis': {
                'type': 'category',
                'data': categories
            },
            'yAxis': {
                'type': 'value'
            },
            'series': series
        })
        
        return config
    
    def _generate_stacked_area_chart(self, data: List[Dict], columns: List[Dict], base_config: Dict) -> Dict:
        """生成堆积面积图配置"""
        config = self._generate_stacked_bar_chart(data, columns, base_config)
        
        # 转换为面积图
        for series_item in config['series']:
            series_item['type'] = 'line'
            series_item['areaStyle'] = {}
        
        config['xAxis']['boundaryGap'] = False
        
        return config
    
    def get_supported_charts(self) -> List[str]:
        """获取支持的图表类型列表"""
        return self.supported_charts