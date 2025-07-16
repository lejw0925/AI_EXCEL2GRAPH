from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum

class DataType(str, Enum):
    """数据类型枚举"""
    DATE = "date"
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"

class ColumnInfo(BaseModel):
    """列信息"""
    name: str = Field(..., description="列名")
    type: DataType = Field(..., description="数据类型")
    sample: Optional[List[str]] = Field(None, description="示例数据")
    unit: Optional[str] = Field(None, description="数据单位")

class HeaderAnalysis(BaseModel):
    """表头分析结果"""
    header_rows: List[int] = Field(..., description="表头所占行索引")
    header_tree: List[Any] = Field(..., description="多级表头树结构")
    data_start_row: int = Field(..., description="数据开始行")
    columns: List[ColumnInfo] = Field(..., description="列信息")
    issues: List[str] = Field(default_factory=list, description="发现的问题")

class ChartRecommendation(BaseModel):
    """图表推荐"""
    chart: str = Field(..., description="图表类型")
    reason: str = Field(..., description="推荐理由")
    score: float = Field(..., ge=0, le=1, description="推荐分数")
    config: Optional[Dict[str, Any]] = Field(None, description="图表配置")

class ChartData(BaseModel):
    """图表数据"""
    recommendations: List[ChartRecommendation] = Field(..., description="图表推荐列表")
    data: List[Dict[str, Any]] = Field(..., description="清洗后的数据")
    columns: List[ColumnInfo] = Field(..., description="列信息")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据信息")

class ExportFormat(str, Enum):
    """导出格式枚举"""
    PNG = "png"
    SVG = "svg"
    PDF = "pdf"
    MARKDOWN = "markdown"
    IFRAME = "iframe"
    PPTX = "pptx"

class ExportOptions(BaseModel):
    """导出选项"""
    format: ExportFormat = Field(..., description="导出格式")
    dpi: Optional[int] = Field(300, description="图片DPI")
    width: Optional[int] = Field(800, description="图片宽度")
    height: Optional[int] = Field(600, description="图片高度")
    title: Optional[str] = Field(None, description="图表标题")

class ExportRequest(BaseModel):
    """导出请求"""
    chart_data: ChartData = Field(..., description="图表数据")
    format: ExportFormat = Field(..., description="导出格式") 
    options: ExportOptions = Field(..., description="导出选项")

class APIResponse(BaseModel):
    """API响应基类"""
    success: bool = Field(..., description="请求是否成功")
    message: Optional[str] = Field(None, description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")
    error: Optional[str] = Field(None, description="错误信息")