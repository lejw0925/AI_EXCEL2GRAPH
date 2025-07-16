export interface ColumnInfo {
  name: string
  type: 'date' | 'number' | 'string' | 'boolean'
  sample?: string[]
  unit?: string
}

export interface HeaderAnalysis {
  header_rows: number[]
  header_tree: any[]
  data_start_row: number
  columns: ColumnInfo[]
  issues: string[]
}

export interface ChartRecommendation {
  chart: string
  reason: string
  score: number
  config?: any
}

export interface ChartData {
  recommendations: ChartRecommendation[]
  data: any[]
  columns: ColumnInfo[]
  selectedChart?: ChartRecommendation
  chartConfig?: any
}

export type ProcessingStep = 
  | 'idle' 
  | 'uploading' 
  | 'analyzing' 
  | 'cleaning' 
  | 'recommending' 
  | 'generating' 
  | 'completed' 
  | 'error'

export interface FileUploadResponse {
  success: boolean
  data?: ChartData
  error?: string
}

export interface ExportOptions {
  format: 'png' | 'svg' | 'pdf' | 'markdown' | 'iframe' | 'pptx'
  dpi?: number
  width?: number
  height?: number
}