#!/bin/bash

# AI图表自动生成工具启动脚本

echo "🚀 启动AI图表自动生成工具..."

# 检查Node.js和Python环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装，请先安装Node.js 16+"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python未安装，请先安装Python 3.8+"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "⚡ 激活虚拟环境..."
source venv/bin/activate

# 安装Python依赖
echo "📥 安装Python依赖..."
pip install -r requirements.txt

# 安装Node.js依赖
echo "📥 安装Node.js依赖..."
npm install

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件，从.env.example复制..."
    cp .env.example .env
    echo "📝 请编辑.env文件配置API密钥"
fi

# 启动后端服务（后台运行）
echo "🔧 启动后端服务..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 5

# 启动前端服务
echo "🎨 启动前端服务..."
npm run dev &
FRONTEND_PID=$!

# 显示访问信息
echo ""
echo "✅ 服务启动完成！"
echo "🌐 前端地址: http://localhost:3000"
echo "🔧 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait