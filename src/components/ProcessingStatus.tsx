import React from 'react'
import { Loader2, Upload, Search, Broom, TrendingUp, BarChart3, AlertCircle } from 'lucide-react'
import { ProcessingStep } from '../types'

interface ProcessingStatusProps {
  step: ProcessingStep
  message: string
}

export const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ step, message }) => {
  const getStepInfo = (currentStep: ProcessingStep) => {
    const steps = [
      { id: 'uploading', label: '上传文件', icon: Upload },
      { id: 'analyzing', label: '分析表头', icon: Search },
      { id: 'cleaning', label: '清洗数据', icon: Broom },
      { id: 'recommending', label: '推荐图表', icon: TrendingUp },
      { id: 'generating', label: '生成图表', icon: BarChart3 }
    ]

    return steps.map(({ id, label, icon: Icon }) => ({
      id,
      label,
      icon: Icon,
      isActive: id === currentStep,
      isCompleted: steps.findIndex(s => s.id === currentStep) > steps.findIndex(s => s.id === id),
      isError: currentStep === 'error'
    }))
  }

  if (step === 'error') {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <AlertCircle className="h-8 w-8 text-red-500" />
            <h3 className="text-xl font-semibold text-red-800 dark:text-red-200">处理失败</h3>
          </div>
          <p className="text-center text-red-700 dark:text-red-300">{message}</p>
        </div>
      </div>
    )
  }

  const stepInfos = getStepInfo(step)

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        <div className="text-center mb-8">
          <Loader2 className="h-12 w-12 text-blue-600 mx-auto mb-4 animate-spin" />
          <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
            正在处理您的文件
          </h3>
          <p className="text-gray-600 dark:text-gray-300">{message}</p>
        </div>

        <div className="flex justify-between items-center mb-8">
          {stepInfos.map(({ id, label, icon: Icon, isActive, isCompleted }, index) => (
            <div key={id} className="flex items-center">
              <div className="flex flex-col items-center">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-colors ${
                    isCompleted
                      ? 'bg-green-500 border-green-500 text-white'
                      : isActive
                      ? 'bg-blue-500 border-blue-500 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-400'
                  }`}
                >
                  {isActive ? (
                    <Loader2 className="h-6 w-6 animate-spin" />
                  ) : (
                    <Icon className="h-6 w-6" />
                  )}
                </div>
                <span
                  className={`mt-2 text-sm font-medium ${
                    isCompleted
                      ? 'text-green-600 dark:text-green-400'
                      : isActive
                      ? 'text-blue-600 dark:text-blue-400'
                      : 'text-gray-500 dark:text-gray-400'
                  }`}
                >
                  {label}
                </span>
              </div>
              
              {index < stepInfos.length - 1 && (
                <div
                  className={`flex-1 h-0.5 mx-4 ${
                    isCompleted ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-600'
                  }`}
                />
              )}
            </div>
          ))}
        </div>

        <div className="text-center text-sm text-gray-500 dark:text-gray-400">
          <p>请稍候，这个过程通常需要5-10秒钟</p>
          <p className="mt-1">AI正在分析您的数据并生成最适合的图表</p>
        </div>
      </div>
    </div>
  )
}