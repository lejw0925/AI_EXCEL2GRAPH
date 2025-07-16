import React from 'react'
import { BarChart3, Github, Heart } from 'lucide-react'

const Header: React.FC = () => {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <BarChart3 className="h-8 w-8 text-blue-600" />
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                AI图表生成器
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                DeepSeek驱动·无需登录·即开即用
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-300">
              <Heart className="h-4 w-4 text-red-500" />
              <span>支持30种图表类型</span>
            </div>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              <Github className="h-5 w-5" />
              <span className="hidden sm:inline">源码</span>
            </a>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header