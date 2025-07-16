# AI图表自动生成工具

> 无登录·全开放·DeepSeek驱动的智能图表生成工具

## 项目简介

这是一个基于Web的AI图表自动生成工具，用户只需上传Excel/CSV文件，系统就能在10秒内完成「表头识别 → 数据清洗 → 图表推荐 → 可视化生成 → 多格式导出」的全流程处理。

### 核心特性

- 🚀 **即开即用**: 无需注册登录，直接使用
- 🤖 **AI驱动**: 基于DeepSeek模型的智能分析
- 📊 **30种图表**: 支持条形图、折线图、饼图等30种图表类型
- 🔧 **智能识别**: 自动识别表头结构和数据类型
- 🧹 **数据清洗**: 自动处理合并单元格、空值等问题
- 📤 **多格式导出**: PNG、SVG、PDF、Markdown、iframe、PowerPoint

## 技术栈

### 前端
- React 18 + TypeScript
- Vite 构建工具
- Tailwind CSS 样式框架
- ECharts 图表库
- React Dropzone 文件上传

### 后端
- Python FastAPI
- Pandas 数据处理
- OpenAI SDK (兼容DeepSeek API)
- Pydantic 数据验证

## 快速开始

### 环境要求

- Node.js 16+ 
- Python 3.8+
- npm/yarn

### 安装步骤

1. **克隆仓库**
```bash
git clone <repository-url>
cd ai-chart-generator
```

2. **安装前端依赖**
```bash
npm install
```

3. **安装后端依赖**
```bash
pip install -r requirements.txt
```

4. **环境配置**
```bash
cp .env.example .env
# 编辑 .env 文件，配置API密钥等信息
```

5. **启动服务**

启动后端服务：
```bash
cd backend
python main.py
```

启动前端服务：
```bash
npm run dev
```

6. **访问应用**

打开浏览器访问 `http://localhost:3000`

## 使用指南

### 支持的文件格式
- Excel: `.xlsx`, `.xls`
- CSV: `.csv`
- TSV: `.tsv`
- ODS: `.ods`
- 最大文件大小: 20MB

### 使用流程

1. **上传文件**: 拖拽或点击上传你的数据文件
2. **等待处理**: AI自动分析表头、清洗数据、推荐图表（约5-10秒）
3. **选择图表**: 从3个AI推荐的图表中选择最合适的
4. **自定义配置**: 调整标题、颜色、图例等设置
5. **导出结果**: 选择需要的格式进行导出

### 支持的图表类型

| 图表类型 | 适用场景 | 数据要求 |
|---------|---------|---------|
| 条形图/柱状图 | 分类数据对比 | 分类 + 数值 |
| 折线图 | 时间趋势分析 | 时间 + 数值 |
| 饼图 | 比例关系展示 | 分类 + 数值 |
| 散点图 | 相关性分析 | 数值 + 数值 |
| 面积图 | 趋势和累计 | 时间 + 数值 |
| 雷达图 | 多维度对比 | 多个数值 |
| 热力图 | 矩阵关系 | 分类 + 分类 + 数值 |
| ... | ... | ... |

## API文档

启动后端服务后，访问 `http://localhost:8000/docs` 查看完整的API文档。

### 主要接口

- `POST /upload` - 上传并处理文件
- `POST /export` - 导出图表
- `GET /health` - 健康检查
- `GET /charts/types` - 获取支持的图表类型

## 配置说明

### DeepSeek API配置

在 `.env` 文件中配置你的DeepSeek API密钥：

```env
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

### 自定义配置

- 修改 `backend/services/ai_analyzer.py` 中的图表推荐逻辑
- 调整 `src/utils/chartConfig.ts` 中的图表配置
- 自定义 `src/index.css` 中的样式主题

## 开发指南

### 项目结构

```
├── src/                    # 前端源码
│   ├── components/         # React组件
│   ├── services/          # API服务
│   ├── types/            # TypeScript类型
│   └── utils/            # 工具函数
├── backend/               # 后端源码
│   ├── models/           # 数据模型
│   ├── services/         # 业务服务
│   └── main.py          # FastAPI入口
├── public/               # 静态资源
└── docs/                # 文档
```

### 添加新图表类型

1. 在 `backend/services/ai_analyzer.py` 中添加图表定义
2. 在 `src/utils/chartConfig.ts` 中实现配置生成
3. 测试和验证新图表类型

### 本地开发

- 前端热重载: `npm run dev`
- 后端热重载: `uvicorn backend.main:app --reload`
- 类型检查: `npm run type-check`
- 代码格式化: `npm run lint`

## 部署指南

### Docker部署

```bash
# 构建镜像
docker build -t ai-chart-generator .

# 运行容器
docker run -p 3000:3000 -p 8000:8000 ai-chart-generator
```

### 云平台部署

支持部署到各大云平台：
- Vercel (前端)
- Railway (后端)
- Heroku
- AWS/阿里云

详细部署指南请参考 `docs/deployment.md`

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add some AmazingFeature'`
4. 推送分支: `git push origin feature/AmazingFeature`
5. 提交Pull Request

## 许可证

本项目基于 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目地址: [GitHub Repository]
- 问题反馈: [GitHub Issues]
- 邮箱联系: [your-email@example.com]

## 更新日志

### v2.0 (2025-01-16)
- 🎉 首次发布
- ✨ 支持30种图表类型
- 🤖 集成DeepSeek AI推荐
- 📊 完整的数据处理流水线
- 🎨 现代化UI设计
- 📤 多格式导出功能

---

**Made with ❤️ by AI Chart Generator Team**