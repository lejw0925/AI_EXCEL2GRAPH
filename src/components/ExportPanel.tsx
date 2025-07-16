import React, { useState } from 'react'
import { Download, Image, FileText, Code, Presentation, Copy, Check } from 'lucide-react'
import { ChartData, ExportOptions } from '../types'

interface ExportPanelProps {
  chartData: ChartData
}

export const ExportPanel: React.FC<ExportPanelProps> = ({ chartData }) => {
  const [exportOptions, setExportOptions] = useState<ExportOptions>({
    format: 'png',
    dpi: 300,
    width: 800,
    height: 600
  })
  const [isExporting, setIsExporting] = useState(false)
  const [copiedText, setCopiedText] = useState<string | null>(null)

  const exportFormats = [
    { id: 'png', label: 'PNG图片', icon: Image, description: '高质量位图，适合插入文档' },
    { id: 'svg', label: 'SVG矢量图', icon: Image, description: '无限缩放的矢量图形' },
    { id: 'pdf', label: 'PDF文档', icon: FileText, description: '可打印的PDF文档' },
    { id: 'markdown', label: 'Markdown', icon: FileText, description: '包含base64图片的Markdown' },
    { id: 'iframe', label: 'iframe嵌入', icon: Code, description: '网页嵌入代码' },
    { id: 'pptx', label: 'PowerPoint', icon: Presentation, description: '矢量图形PPT文件' }
  ]

  const handleExport = async (format: string) => {
    setIsExporting(true)
    try {
      // 这里调用后端API进行导出
      const response = await fetch('/api/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chartData,
          format,
          options: exportOptions
        })
      })

      if (format === 'markdown' || format === 'iframe') {
        const text = await response.text()
        await navigator.clipboard.writeText(text)
        setCopiedText(format)
        setTimeout(() => setCopiedText(null), 2000)
      } else {
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `chart.${format}`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
      }
    } catch (error) {
      console.error('Export failed:', error)
    } finally {
      setIsExporting(false)
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center space-x-2 mb-6">
        <Download className="h-6 w-6 text-blue-600" />
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">导出图表</h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {exportFormats.map(({ id, label, icon: Icon, description }) => (
          <div
            key={id}
            onClick={() => setExportOptions(prev => ({ ...prev, format: id as any }))}
            className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
              exportOptions.format === id
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-200 dark:border-gray-600 hover:border-blue-300'
            }`}
          >
            <div className="flex items-center space-x-3 mb-2">
              <Icon className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-gray-900 dark:text-white">{label}</span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-300">{description}</p>
          </div>
        ))}
      </div>

      {/* 导出选项 */}
      {(exportOptions.format === 'png' || exportOptions.format === 'svg' || exportOptions.format === 'pdf') && (
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6">
          <h4 className="font-medium text-gray-900 dark:text-white mb-3">导出设置</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                宽度 (px)
              </label>
              <input
                type="number"
                value={exportOptions.width}
                onChange={(e) => setExportOptions(prev => ({ ...prev, width: parseInt(e.target.value) }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                高度 (px)
              </label>
              <input
                type="number"
                value={exportOptions.height}
                onChange={(e) => setExportOptions(prev => ({ ...prev, height: parseInt(e.target.value) }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
            {exportOptions.format === 'png' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  DPI
                </label>
                <select
                  value={exportOptions.dpi}
                  onChange={(e) => setExportOptions(prev => ({ ...prev, dpi: parseInt(e.target.value) }))}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                >
                  <option value={72}>72 DPI (网页)</option>
                  <option value={150}>150 DPI (标准)</option>
                  <option value={300}>300 DPI (高质量)</option>
                  <option value={600}>600 DPI (打印)</option>
                </select>
              </div>
            )}
          </div>
        </div>
      )}

      {/* 导出按钮 */}
      <div className="flex justify-center">
        <button
          onClick={() => handleExport(exportOptions.format)}
          disabled={isExporting}
          className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isExporting ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>导出中...</span>
            </>
          ) : copiedText === exportOptions.format ? (
            <>
              <Check className="h-4 w-4" />
              <span>已复制到剪贴板</span>
            </>
          ) : (
            <>
              {exportOptions.format === 'markdown' || exportOptions.format === 'iframe' ? (
                <Copy className="h-4 w-4" />
              ) : (
                <Download className="h-4 w-4" />
              )}
              <span>
                {exportOptions.format === 'markdown' || exportOptions.format === 'iframe' 
                  ? '复制代码' 
                  : `导出${exportFormats.find(f => f.id === exportOptions.format)?.label}`
                }
              </span>
            </>
          )}
        </button>
      </div>

      {/* 快速导出按钮 */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
        <p className="text-sm text-gray-600 dark:text-gray-300 mb-3 text-center">快速导出</p>
        <div className="flex justify-center space-x-2">
          {['png', 'svg', 'pdf'].map(format => (
            <button
              key={format}
              onClick={() => handleExport(format)}
              className="px-4 py-2 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              {format.toUpperCase()}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}