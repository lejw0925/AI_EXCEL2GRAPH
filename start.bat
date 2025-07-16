@echo off
chcp 65001 >nul
echo 🚀 启动AI图表自动生成工具...

REM 检查Node.js环境
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装，请先安装Node.js 16+
    pause
    exit /b 1
)

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 创建虚拟环境（如果不存在）
if not exist "venv" (
    echo 📦 创建Python虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo ⚡ 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装Python依赖
echo 📥 安装Python依赖...
pip install -r requirements.txt

REM 安装Node.js依赖
echo 📥 安装Node.js依赖...
npm install

REM 检查环境变量文件
if not exist ".env" (
    echo ⚠️  未找到.env文件，从.env.example复制...
    copy .env.example .env
    echo 📝 请编辑.env文件配置API密钥
)

REM 启动后端服务
echo 🔧 启动后端服务...
start /b cmd /c "cd backend && python main.py"

REM 等待后端启动
timeout /t 5 /nobreak >nul

REM 启动前端服务
echo 🎨 启动前端服务...
start /b cmd /c "npm run dev"

echo.
echo ✅ 服务启动完成！
echo 🌐 前端地址: http://localhost:3000
echo 🔧 后端API: http://localhost:8000
echo 📚 API文档: http://localhost:8000/docs
echo.
echo 按任意键停止服务...
pause >nul