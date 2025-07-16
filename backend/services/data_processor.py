import pandas as pd
import numpy as np
import io
import logging
from typing import Tuple, Dict, List, Any
from datetime import datetime
import re
import openpyxl
from openpyxl import load_workbook

logger = logging.getLogger(__name__)

class DataProcessor:
    """数据处理器"""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls', '.csv', '.tsv', '.ods']
    
    async def analyze_file(self, content: bytes, filename: str) -> Tuple[pd.DataFrame, Dict]:
        """
        分析文件并识别表头结构
        
        Args:
            content: 文件内容
            filename: 文件名
            
        Returns:
            DataFrame和表头分析结果
        """
        try:
            # 根据文件类型读取数据
            df = await self._read_file(content, filename)
            
            # 分析表头结构
            header_analysis = await self._analyze_header_structure(df)
            
            return df, header_analysis
            
        except Exception as e:
            logger.error(f"文件分析失败: {str(e)}")
            raise
    
    async def _read_file(self, content: bytes, filename: str) -> pd.DataFrame:
        """读取不同格式的文件"""
        file_ext = '.' + filename.split('.')[-1].lower()
        
        try:
            if file_ext in ['.xlsx', '.xls']:
                # Excel文件
                return pd.read_excel(io.BytesIO(content), header=None)
            elif file_ext == '.csv':
                # CSV文件，尝试不同编码
                for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                    try:
                        content_str = content.decode(encoding)
                        return pd.read_csv(io.StringIO(content_str), header=None)
                    except UnicodeDecodeError:
                        continue
                raise ValueError("无法解码CSV文件")
            elif file_ext == '.tsv':
                # TSV文件
                content_str = content.decode('utf-8')
                return pd.read_csv(io.StringIO(content_str), sep='\t', header=None)
            elif file_ext == '.ods':
                # ODS文件
                return pd.read_excel(io.BytesIO(content), engine='odf', header=None)
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
                
        except Exception as e:
            logger.error(f"读取文件失败: {str(e)}")
            raise
    
    async def _analyze_header_structure(self, df: pd.DataFrame) -> Dict:
        """分析表头结构"""
        try:
            issues = []
            header_rows = [0]  # 默认第一行为表头
            data_start_row = 1
            
            # 检测合并单元格和多级表头
            if self._has_merged_cells(df):
                issues.append("检测到合并单元格")
                header_rows = [0, 1]  # 可能有多级表头
                data_start_row = 2
            
            # 检测空行
            empty_rows = df.isnull().all(axis=1)
            if empty_rows.any():
                empty_row_indices = empty_rows[empty_rows].index.tolist()
                issues.append(f"发现空行: {empty_row_indices}")
            
            # 分析列信息
            columns_info = await self._analyze_columns(df, data_start_row)
            
            return {
                "header_rows": header_rows,
                "header_tree": [],  # 简化实现
                "data_start_row": data_start_row,
                "columns": columns_info,
                "issues": issues
            }
            
        except Exception as e:
            logger.error(f"表头分析失败: {str(e)}")
            raise
    
    def _has_merged_cells(self, df: pd.DataFrame) -> bool:
        """检测是否有合并单元格（简化检测）"""
        # 检查前几行是否有重复的非空值，可能表示合并单元格
        for i in range(min(3, len(df))):
            row = df.iloc[i]
            non_null_values = row.dropna()
            if len(non_null_values) != len(set(non_null_values.astype(str))):
                return True
        return False
    
    async def _analyze_columns(self, df: pd.DataFrame, data_start_row: int) -> List[Dict]:
        """分析列信息和数据类型"""
        columns_info = []
        
        # 获取表头名称
        header_row = df.iloc[0] if data_start_row > 0 else df.columns
        
        for i, col_name in enumerate(header_row):
            if pd.isna(col_name):
                col_name = f"列{i+1}"
            
            # 获取该列的数据样本
            if data_start_row < len(df):
                col_data = df.iloc[data_start_row:, i].dropna()
            else:
                col_data = pd.Series([])
            
            # 推断数据类型
            data_type = self._infer_data_type(col_data)
            
            # 获取样本数据
            sample_data = col_data.head(3).astype(str).tolist() if len(col_data) > 0 else []
            
            columns_info.append({
                "name": str(col_name),
                "type": data_type,
                "sample": sample_data,
                "unit": self._extract_unit(str(col_name))
            })
        
        return columns_info
    
    def _infer_data_type(self, series: pd.Series) -> str:
        """推断数据类型"""
        if len(series) == 0:
            return "string"
        
        # 尝试转换为数值
        try:
            pd.to_numeric(series, errors='raise')
            return "number"
        except (ValueError, TypeError):
            pass
        
        # 尝试转换为日期
        try:
            pd.to_datetime(series, errors='raise')
            return "date"
        except (ValueError, TypeError):
            pass
        
        # 检查布尔值
        unique_values = set(series.astype(str).str.lower().unique())
        boolean_values = {'true', 'false', '是', '否', '0', '1', 'yes', 'no'}
        if unique_values.issubset(boolean_values):
            return "boolean"
        
        return "string"
    
    def _extract_unit(self, column_name: str) -> str:
        """从列名中提取单位"""
        # 使用正则表达式提取括号中的单位
        match = re.search(r'\(([^)]+)\)', column_name)
        if match:
            return match.group(1)
        
        # 检查常见单位
        units = ['元', '万元', '亿元', '%', '个', '人', '次', '天', '月', '年', 'kg', 'g', 'm', 'cm']
        for unit in units:
            if unit in column_name:
                return unit
        
        return None
    
    async def clean_data(self, df: pd.DataFrame, header_analysis: Dict) -> Tuple[pd.DataFrame, List[Dict]]:
        """清洗数据"""
        try:
            data_start_row = header_analysis['data_start_row']
            columns_info = header_analysis['columns']
            
            # 提取数据部分
            data_df = df.iloc[data_start_row:].copy()
            
            # 设置列名
            data_df.columns = [col['name'] for col in columns_info[:len(data_df.columns)]]
            
            # 删除完全空的行和列
            data_df = data_df.dropna(how='all')
            data_df = data_df.dropna(axis=1, how='all')
            
            # 根据数据类型清洗数据
            for col_info in columns_info:
                col_name = col_info['name']
                if col_name not in data_df.columns:
                    continue
                    
                col_type = col_info['type']
                
                if col_type == 'number':
                    # 清洗数值列
                    data_df[col_name] = self._clean_numeric_column(data_df[col_name])
                elif col_type == 'date':
                    # 清洗日期列
                    data_df[col_name] = self._clean_date_column(data_df[col_name])
                elif col_type == 'boolean':
                    # 清洗布尔列
                    data_df[col_name] = self._clean_boolean_column(data_df[col_name])
            
            # 重置索引
            data_df.reset_index(drop=True, inplace=True)
            
            # 更新列信息
            updated_columns_info = []
            for col_name in data_df.columns:
                original_col = next((col for col in columns_info if col['name'] == col_name), None)
                if original_col:
                    updated_columns_info.append(original_col)
            
            logger.info(f"数据清洗完成，剩余{len(data_df)}行，{len(data_df.columns)}列")
            return data_df, updated_columns_info
            
        except Exception as e:
            logger.error(f"数据清洗失败: {str(e)}")
            raise
    
    def _clean_numeric_column(self, series: pd.Series) -> pd.Series:
        """清洗数值列"""
        # 移除非数值字符，保留数字、小数点、负号
        cleaned = series.astype(str).str.replace(r'[^\d.-]', '', regex=True)
        # 转换为数值，无法转换的设为NaN
        return pd.to_numeric(cleaned, errors='coerce')
    
    def _clean_date_column(self, series: pd.Series) -> pd.Series:
        """清洗日期列"""
        # 尝试转换为日期时间
        return pd.to_datetime(series, errors='coerce')
    
    def _clean_boolean_column(self, series: pd.Series) -> pd.Series:
        """清洗布尔列"""
        # 标准化布尔值
        mapping = {
            'true': True, 'false': False,
            '是': True, '否': False,
            'yes': True, 'no': False,
            '1': True, '0': False
        }
        
        normalized = series.astype(str).str.lower().map(mapping)
        return normalized