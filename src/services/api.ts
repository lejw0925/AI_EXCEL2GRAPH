import axios from 'axios'
import { FileUploadResponse, ChartData, ExportOptions } from '../types'

const API_BASE_URL = '/api'

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30秒超时
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

/**
 * 上传文件并处理
 */
export const uploadFile = async (file: File): Promise<FileUploadResponse> => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    return {
      success: true,
      data: response.data
    }
  } catch (error: any) {
    return {
      success: false,
      error: error.response?.data?.error || error.message || '上传失败'
    }
  }
}

/**
 * 导出图表
 */
export const exportChart = async (
  chartData: ChartData, 
  format: string, 
  options: ExportOptions
): Promise<Blob | string> => {
  try {
    const response = await api.post('/export', {
      chartData,
      format,
      options
    }, {
      responseType: format === 'markdown' || format === 'iframe' ? 'text' : 'blob'
    })

    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || error.message || '导出失败')
  }
}

/**
 * 获取图表配置
 */
export const getChartConfig = async (chartType: string, data: any[], columns: any[]): Promise<any> => {
  try {
    const response = await api.post('/chart-config', {
      chartType,
      data,
      columns
    })

    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || error.message || '获取图表配置失败')
  }
}

export default api