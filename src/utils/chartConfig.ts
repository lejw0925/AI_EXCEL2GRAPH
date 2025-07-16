import { ColumnInfo } from '../types'

// 颜色主题
const COLOR_THEMES = [
  ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'], // 蓝色系
  ['#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d3'], // 绿色系  
  ['#d62728', '#ff9896', '#2ca02c', '#98df8a', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d3'], // 红色系
  ['#9467bd', '#c5b0d5', '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896'], // 紫色系
  ['#ff7f0e', '#ffbb78', '#d62728', '#ff9896', '#2ca02c', '#98df8a', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94'], // 橙色系
  ['#17becf', '#9edae5', '#1f77b4', '#aec7e8', '#2ca02c', '#98df8a', '#ff7f0e', '#ffbb78', '#d62728', '#ff9896']  // 青色系
]

/**
 * 生成图表配置
 */
export const generateChartConfig = (
  chartType: string, 
  data: any[], 
  columns: ColumnInfo[], 
  customConfig: any = {}
): any => {
  const colors = COLOR_THEMES[customConfig.colorTheme || 0]
  
  const baseConfig = {
    backgroundColor: 'transparent',
    color: colors,
    title: {
      text: customConfig.title || '',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      show: customConfig.legendPosition !== 'none',
      orient: customConfig.legendPosition === 'left' || customConfig.legendPosition === 'right' ? 'vertical' : 'horizontal',
      left: customConfig.legendPosition === 'left' ? 'left' : customConfig.legendPosition === 'right' ? 'right' : 'center',
      top: customConfig.legendPosition === 'top' ? 'top' : customConfig.legendPosition === 'bottom' ? 'bottom' : 'auto'
    },
    grid: {
      show: customConfig.showGrid !== false,
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    }
  }

  switch (chartType) {
    case '条形图':
    case '柱状图':
      return generateBarChart(data, columns, baseConfig, chartType === '条形图')
    
    case '折线图':
      return generateLineChart(data, columns, baseConfig)
    
    case '饼图':
      return generatePieChart(data, columns, baseConfig)
    
    case '散点图':
      return generateScatterChart(data, columns, baseConfig)
    
    case '面积图':
      return generateAreaChart(data, columns, baseConfig)
    
    case '雷达图':
      return generateRadarChart(data, columns, baseConfig)
    
    case '热力图':
      return generateHeatmapChart(data, columns, baseConfig)
    
    case '漏斗图':
      return generateFunnelChart(data, columns, baseConfig)
    
    case '堆积条形图':
      return generateStackedBarChart(data, columns, baseConfig)
    
    case '堆积面积图':
      return generateStackedAreaChart(data, columns, baseConfig)
    
    default:
      return generateBarChart(data, columns, baseConfig)
  }
}

/**
 * 生成条形图/柱状图配置
 */
function generateBarChart(data: any[], columns: ColumnInfo[], baseConfig: any, isHorizontal = false): any {
  const categoryCol = columns.find(col => col.type === 'string') || columns[0]
  const valueCol = columns.find(col => col.type === 'number') || columns[1]
  
  const categories = data.map(row => row[categoryCol.name])
  const values = data.map(row => row[valueCol.name])

  return {
    ...baseConfig,
    xAxis: {
      type: isHorizontal ? 'value' : 'category',
      data: isHorizontal ? undefined : categories,
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: isHorizontal ? 'category' : 'value',
      data: isHorizontal ? categories : undefined
    },
    series: [{
      name: valueCol.name,
      type: 'bar',
      data: values,
      emphasis: {
        focus: 'series'
      }
    }]
  }
}

/**
 * 生成折线图配置
 */
function generateLineChart(data: any[], columns: ColumnInfo[], baseConfig: any): any {
  const xCol = columns.find(col => col.type === 'date' || col.type === 'string') || columns[0]
  const yCol = columns.find(col => col.type === 'number') || columns[1]
  
  const xData = data.map(row => row[xCol.name])
  const yData = data.map(row => row[yCol.name])

  return {
    ...baseConfig,
    xAxis: {
      type: 'category',
      data: xData,
      boundaryGap: false
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      name: yCol.name,
      type: 'line',
      data: yData,
      smooth: true,
      emphasis: {
        focus: 'series'
      }
    }]
  }
}

/**
 * 生成饼图配置
 */
function generatePieChart(data: any[], columns: ColumnInfo[], baseConfig: any): any {
  const nameCol = columns.find(col => col.type === 'string') || columns[0]
  const valueCol = columns.find(col => col.type === 'number') || columns[1]
  
  const pieData = data.map(row => ({
    name: row[nameCol.name],
    value: row[valueCol.name]
  }))

  return {
    ...baseConfig,
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [{
      name: nameCol.name,
      type: 'pie',
      radius: '50%',
      data: pieData,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
}

/**
 * 生成散点图配置
 */
function generateScatterChart(data: any[], columns: ColumnInfo[], baseConfig: any): any {
  const xCol = columns.find(col => col.type === 'number') || columns[0]
  const yCol = columns.find(col => col.type === 'number' && col.name !== xCol.name) || columns[1]
  
  const scatterData = data.map(row => [row[xCol.name], row[yCol.name]])

  return {
    ...baseConfig,
    xAxis: {
      type: 'value',
      name: xCol.name,
      nameLocation: 'middle',
      nameGap: 30
    },
    yAxis: {
      type: 'value',
      name: yCol.name,
      nameLocation: 'middle',
      nameGap: 50
    },
    series: [{
      name: `${xCol.name} vs ${yCol.name}`,
      type: 'scatter',
      data: scatterData,
      symbolSize: 8,
      emphasis: {
        focus: 'series'
      }
    }]
  }
}

/**
 * 生成面积图配置
 */
function generateAreaChart(data: any[], columns: ColumnInfo[], baseConfig: any): any {
  const xCol = columns.find(col => col.type === 'date' || col.type === 'string') || columns[0]
  const yCol = columns.find(col => col.type === 'number') || columns[1]
  
  const xData = data.map(row => row[xCol.name])
  const yData = data.map(row => row[yCol.name])

  return {
    ...baseConfig,
    xAxis: {
      type: 'category',
      data: xData,
      boundaryGap: false
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      name: yCol.name,
      type: 'line',
      data: yData,
      areaStyle: {
        opacity: 0.6
      },
      smooth: true,
      emphasis: {
        focus: 'series'
      }
    }]
  }
}

/**
 * 生成雷达图配置
 */
function generateRadarChart(data: any[], columns: ColumnInfo[], baseConfig: any): any {
  const indicators = columns.filter(col => col.type === 'number').map(col => ({
    name: col.name,
    max: Math.max(...data.map(row => row[col.name])) * 1.2
  }))
  
  const radarData = data.map((row, index) => ({
    value: indicators.map(indicator => row[indicator.name]),
    name: `数据${index + 1}`
  }))

  return {
    ...baseConfig,
    radar: {
      indicator: indicators
    },
    series: [{
      name: '雷达图',
      type: 'radar',
      data: radarData
    }]
  }
}

/**
 * 生成热力图配置
 */
function generateHeatmapChart(data: any[], columns: ColumnInfo[], baseConfig: any): any {
  // 简化的热力图实现
  const xCol = columns[0]
  const yCol = columns[1]
  const valueCol = columns.find(col => col.type === 'number') || columns[2]
  
  const heatmapData = data.map((row, xIndex) => 
    data.map((_, yIndex) => [xIndex, yIndex, row[valueCol.name] || 0])
  ).flat()

  return {
    ...baseConfig,
    xAxis: {
      type: 'category',
      data: [...new Set(data.map(row => row[xCol.name]))]
    },
    yAxis: {
      type: 'category',
      data: [...new Set(data.map(row => row[yCol.name]))]
    },
    visualMap: {
      min: 0,
      max: Math.max(...data.map(row => row[valueCol.name] || 0)),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '15%'
    },
    series: [{
      name: valueCol.name,
      type: 'heatmap',
      data: heatmapData,
      label: {
        show: true
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
}

/**
 * 生成漏斗图配置
 */
function generateFunnelChart(data: any[], columns: ColumnInfo[], baseConfig: any): any {
  const nameCol = columns.find(col => col.type === 'string') || columns[0]
  const valueCol = columns.find(col => col.type === 'number') || columns[1]
  
  const funnelData = data.map(row => ({
    name: row[nameCol.name],
    value: row[valueCol.name]
  })).sort((a, b) => b.value - a.value)

  return {
    ...baseConfig,
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [{
      name: nameCol.name,
      type: 'funnel',
      left: '10%',
      top: 60,
      bottom: 60,
      width: '80%',
      data: funnelData
    }]
  }
}

/**
 * 生成堆积条形图配置
 */
function generateStackedBarChart(data: any[], columns: ColumnInfo[], baseConfig: any): any {
  const categoryCol = columns.find(col => col.type === 'string') || columns[0]
  const valueColumns = columns.filter(col => col.type === 'number')
  
  const categories = [...new Set(data.map(row => row[categoryCol.name]))]
  
  const series = valueColumns.map(col => ({
    name: col.name,
    type: 'bar',
    stack: 'total',
    data: categories.map(cat => {
      const row = data.find(r => r[categoryCol.name] === cat)
      return row ? row[col.name] : 0
    })
  }))

  return {
    ...baseConfig,
    xAxis: {
      type: 'category',
      data: categories
    },
    yAxis: {
      type: 'value'
    },
    series
  }
}

/**
 * 生成堆积面积图配置
 */
function generateStackedAreaChart(data: any[], columns: ColumnInfo[], baseConfig: any): any {
  const xCol = columns.find(col => col.type === 'date' || col.type === 'string') || columns[0]
  const valueColumns = columns.filter(col => col.type === 'number')
  
  const xData = [...new Set(data.map(row => row[xCol.name]))]
  
  const series = valueColumns.map(col => ({
    name: col.name,
    type: 'line',
    stack: 'total',
    areaStyle: {},
    data: xData.map(x => {
      const row = data.find(r => r[xCol.name] === x)
      return row ? row[col.name] : 0
    })
  }))

  return {
    ...baseConfig,
    xAxis: {
      type: 'category',
      data: xData,
      boundaryGap: false
    },
    yAxis: {
      type: 'value'
    },
    series
  }
}