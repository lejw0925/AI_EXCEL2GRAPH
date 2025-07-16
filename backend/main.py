from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, PlainTextResponse
import pandas as pd
import numpy as np
import io
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from .services.data_processor import DataProcessor
from .services.ai_analyzer import AIAnalyzer
from .services.chart_generator import ChartGenerator
from .services.export_service import ExportService
from .models.schemas import ChartData, ExportRequest, ChartRecommendation

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="AI图表自动生成工具",
    description="无登录·全开放·DeepSeek驱动的智能图表生成工具",
    version="2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
data_processor = DataProcessor()
ai_analyzer = AIAnalyzer()
chart_generator = ChartGenerator()
export_service = ExportService()

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "AI图表自动生成工具 API",
        "version": "2.0",
        "powered_by": "DeepSeek",
        "features": [
            "智能表头识别",
            "自动数据清洗", 
            "AI图表推荐",
            "30种图表类型",
            "多格式导出"
        ],
        "endpoints": {
            "upload": "/upload - 上传并处理文件",
            "export": "/export - 导出图表",
            "health": "/health - 健康检查"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "data_processor": "ok",
            "ai_analyzer": "ok", 
            "chart_generator": "ok",
            "export_service": "ok"
        }
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    上传文件并进行AI分析处理
    
    支持的文件格式：
    - Excel: .xlsx, .xls
    - CSV: .csv
    - TSV: .tsv  
    - ODS: .ods
    """
    try:
        logger.info(f"接收到文件: {file.filename}, 大小: {file.size} bytes")
        
        # 检查文件类型
        if not file.filename:
            raise HTTPException(status_code=400, detail="文件名为空")
            
        allowed_extensions = ['.xlsx', '.xls', '.csv', '.tsv', '.ods']
        file_extension = '.' + file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的文件格式。支持的格式: {', '.join(allowed_extensions)}"
            )
        
        # 检查文件大小 (20MB限制)
        if file.size > 20 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="文件大小超过20MB限制")
        
        # 读取文件内容
        content = await file.read()
        
        # Step 1: 表头识别和数据加载
        logger.info("开始分析表头结构...")
        df, header_analysis = await data_processor.analyze_file(content, file.filename)
        
        # Step 2: 数据清洗
        logger.info("开始清洗数据...")
        cleaned_df, columns_info = await data_processor.clean_data(df, header_analysis)
        
        # Step 3: AI图表推荐
        logger.info("开始AI图表推荐...")
        recommendations = await ai_analyzer.recommend_charts(cleaned_df, columns_info)
        
        # Step 4: 准备返回数据
        result_data = {
            "recommendations": recommendations,
            "data": cleaned_df.to_dict('records'),
            "columns": columns_info,
            "metadata": {
                "original_filename": file.filename,
                "rows_count": len(cleaned_df),
                "columns_count": len(columns_info),
                "file_size": file.size,
                "processing_time": datetime.now().isoformat(),
                "issues_found": header_analysis.get("issues", [])
            }
        }
        
        logger.info(f"文件处理完成，生成{len(recommendations)}个图表推荐")
        return result_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"文件处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

@app.post("/export")
async def export_chart(request: ExportRequest):
    """
    导出图表
    
    支持的导出格式：
    - PNG: 高质量位图
    - SVG: 矢量图形
    - PDF: PDF文档
    - Markdown: 包含base64图片的Markdown
    - iframe: HTML嵌入代码
    - PowerPoint: PPT文件
    """
    try:
        logger.info(f"开始导出图表，格式: {request.format}")
        
        # 生成图表配置
        chart_config = chart_generator.generate_config(
            request.chart_data.recommendations[0].chart,
            request.chart_data.data,
            request.chart_data.columns,
            request.options.__dict__ if hasattr(request.options, '__dict__') else {}
        )
        
        # 根据格式导出
        if request.format in ['markdown', 'iframe']:
            # 返回文本内容
            result = await export_service.export_text(
                chart_config, 
                request.format, 
                request.options
            )
            return PlainTextResponse(content=result)
        else:
            # 返回二进制文件
            file_content, mime_type = await export_service.export_binary(
                chart_config,
                request.format, 
                request.options
            )
            
            filename = f"chart.{request.format}"
            
            return StreamingResponse(
                io.BytesIO(file_content),
                media_type=mime_type,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
            
    except Exception as e:
        logger.error(f"导出失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")

@app.post("/chart-config")
async def get_chart_config(request: Dict[str, Any]):
    """获取图表配置"""
    try:
        chart_type = request.get("chartType")
        data = request.get("data", [])
        columns = request.get("columns", [])
        
        config = chart_generator.generate_config(chart_type, data, columns)
        return config
        
    except Exception as e:
        logger.error(f"获取图表配置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取图表配置失败: {str(e)}")

@app.get("/charts/types")
async def get_supported_chart_types():
    """获取支持的图表类型列表"""
    return chart_generator.get_supported_charts()

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    logger.error(f"未处理的异常: {str(exc)}")
    return {"error": "服务器内部错误", "detail": str(exc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)