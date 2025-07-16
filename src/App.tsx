import React, { useState } from 'react'
import FileUpload from './components/FileUpload'
import ChartDisplay from './components/ChartDisplay'
import Header from './components/Header'
import { ProcessingStatus } from './components/ProcessingStatus'
import { ExportPanel } from './components/ExportPanel'
import { ChartData, ProcessingStep } from './types'

function App() {
  const [chartData, setChartData] = useState<ChartData | null>(null)
  const [processingStep, setProcessingStep] = useState<ProcessingStep>('idle')
  const [processingMessage, setProcessingMessage] = useState('')

  const handleFileUploaded = (data: ChartData) => {
    setChartData(data)
    setProcessingStep('completed')
  }

  const handleProcessingUpdate = (step: ProcessingStep, message: string) => {
    setProcessingStep(step)
    setProcessingMessage(message)
  }

  const resetData = () => {
    setChartData(null)
    setProcessingStep('idle')
    setProcessingMessage('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {processingStep === 'idle' && (
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              AI图表自动生成工具
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-2">
              无登录·全开放·DeepSeek驱动
            </p>
            <p className="text-lg text-gray-500 dark:text-gray-400">
              上传任意Excel/CSV，10秒内完成智能图表生成
            </p>
          </div>
        )}

        {processingStep !== 'idle' && processingStep !== 'completed' && (
          <ProcessingStatus step={processingStep} message={processingMessage} />
        )}

        {processingStep === 'idle' && (
          <FileUpload 
            onFileUploaded={handleFileUploaded}
            onProcessingUpdate={handleProcessingUpdate}
          />
        )}

        {chartData && processingStep === 'completed' && (
          <div className="space-y-8">
            <ChartDisplay chartData={chartData} />
            <ExportPanel chartData={chartData} />
            <div className="text-center">
              <button
                onClick={resetData}
                className="px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                重新上传文件
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App