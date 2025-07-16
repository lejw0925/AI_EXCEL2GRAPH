import React, { useState, useRef } from 'react'
import ReactECharts from 'echarts-for-react'
import { ChartData, ChartRecommendation } from '../types'
import { generateChartConfig } from '../utils/chartConfig'
import { Palette, Settings, RotateCcw } from 'lucide-react'

interface ChartDisplayProps {
  chartData: ChartData
}

const ChartDisplay: React.FC<ChartDisplayProps> = ({ chartData }) => {
  const [selectedChart, setSelectedChart] = useState<ChartRecommendation>(
    chartData.selectedChart || chartData.recommendations[0]
  )
  const [customConfig, setCustomConfig] = useState<any>({})
  const chartRef = useRef<ReactECharts>(null)

  const chartConfig = generateChartConfig(selectedChart.chart, chartData.data, chartData.columns, customConfig)

  const handleChartSelect = (chart: ChartRecommendation) => {
    setSelectedChart(chart)
    setCustomConfig({}) // 重置自定义配置
  }

  const updateConfig = (key: string, value: any) => {
    setCustomConfig(prev => ({
      ...prev,
      [key]: value
    }))
  }

  return (
    <div className="space-y-6">
      {/* 图表推荐选择 */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          AI推荐图表 (共{chartData.recommendations.length}种)
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {chartData.recommendations.map((chart, index) => (
            <div
              key={index}
              onClick={() => handleChartSelect(chart)}
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                selectedChart.chart === chart.chart
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-gray-600 hover:border-blue-300'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-gray-900 dark:text-white">{chart.chart}</h4>
                <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">
                  {Math.round(chart.score * 100)}%
                </span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-300">{chart.reason}</p>
            </div>
          ))}
        </div>
      </div>

      {/* 图表显示区域 */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* 图表 */}
        <div className="lg:col-span-3">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                {selectedChart.chart}
              </h3>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setCustomConfig({})}
                  className="p-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
                  title="重置配置"
                >
                  <RotateCcw className="h-4 w-4" />
                </button>
              </div>
            </div>
            
            <div className="h-96">
              <ReactECharts
                ref={chartRef}
                option={chartConfig}
                style={{ height: '100%', width: '100%' }}
                opts={{ renderer: 'canvas' }}
              />
            </div>
          </div>
        </div>

        {/* 配置面板 */}
        <div className="space-y-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
            <div className="flex items-center space-x-2 mb-4">
              <Settings className="h-5 w-5 text-gray-500" />
              <h4 className="font-medium text-gray-900 dark:text-white">图表配置</h4>
            </div>
            
            <div className="space-y-4">
              {/* 标题设置 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  图表标题
                </label>
                <input
                  type="text"
                  value={customConfig.title || ''}
                  onChange={(e) => updateConfig('title', e.target.value)}
                  placeholder="请输入图表标题"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>

              {/* 颜色主题 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  颜色主题
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {['蓝色', '绿色', '红色', '紫色', '橙色', '青色'].map((color, index) => (
                    <button
                      key={color}
                      onClick={() => updateConfig('colorTheme', index)}
                      className={`p-2 text-xs rounded border ${
                        customConfig.colorTheme === index
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                          : 'border-gray-300 dark:border-gray-600'
                      }`}
                    >
                      {color}
                    </button>
                  ))}
                </div>
              </div>

              {/* 图表尺寸 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  显示网格
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={customConfig.showGrid !== false}
                    onChange={(e) => updateConfig('showGrid', e.target.checked)}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-600 dark:text-gray-300">显示网格线</span>
                </label>
              </div>

              {/* 图例设置 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  图例位置
                </label>
                <select
                  value={customConfig.legendPosition || 'top'}
                  onChange={(e) => updateConfig('legendPosition', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="top">顶部</option>
                  <option value="bottom">底部</option>
                  <option value="left">左侧</option>
                  <option value="right">右侧</option>
                  <option value="none">不显示</option>
                </select>
              </div>
            </div>
          </div>

          {/* 数据信息 */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
            <h4 className="font-medium text-gray-900 dark:text-white mb-3">数据信息</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">总行数:</span>
                <span className="font-medium text-gray-900 dark:text-white">{chartData.data.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">列数:</span>
                <span className="font-medium text-gray-900 dark:text-white">{chartData.columns.length}</span>
              </div>
              <div className="pt-2 border-t border-gray-200 dark:border-gray-600">
                <span className="text-gray-600 dark:text-gray-300">列信息:</span>
                <ul className="mt-1 space-y-1">
                  {chartData.columns.map((col, index) => (
                    <li key={index} className="text-xs">
                      <span className="font-medium text-gray-900 dark:text-white">{col.name}</span>
                      <span className="ml-2 text-gray-500 dark:text-gray-400">({col.type})</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChartDisplay