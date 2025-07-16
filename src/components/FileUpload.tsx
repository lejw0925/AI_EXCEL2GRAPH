import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, AlertCircle } from 'lucide-react'
import { ChartData, ProcessingStep } from '../types'
import { uploadFile } from '../services/api'

interface FileUploadProps {
  onFileUploaded: (data: ChartData) => void
  onProcessingUpdate: (step: ProcessingStep, message: string) => void
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUploaded, onProcessingUpdate }) => {
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    setError(null)

    try {
      onProcessingUpdate('uploading', '正在上传文件...')
      
      // 模拟处理步骤
      setTimeout(() => onProcessingUpdate('analyzing', '正在分析表头结构...'), 1000)
      setTimeout(() => onProcessingUpdate('cleaning', '正在清洗数据...'), 3000)
      setTimeout(() => onProcessingUpdate('recommending', '正在推荐图表类型...'), 5000)
      setTimeout(() => onProcessingUpdate('generating', '正在生成图表...'), 7000)

      const result = await uploadFile(file)
      
      if (result.success && result.data) {
        onFileUploaded(result.data)
      } else {
        setError(result.error || '文件处理失败')
        onProcessingUpdate('error', result.error || '文件处理失败')
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '上传失败'
      setError(errorMessage)
      onProcessingUpdate('error', errorMessage)
    }
  }, [onFileUploaded, onProcessingUpdate])

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv'],
      'text/tab-separated-values': ['.tsv'],
      'application/vnd.oasis.opendocument.spreadsheet': ['.ods']
    },
    maxSize: 20 * 1024 * 1024, // 20MB
    multiple: false
  })

  return (
    <div className="max-w-4xl mx-auto">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-blue-400 bg-blue-50 dark:bg-blue-900/20'
            : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20'
        }`}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          <Upload className="h-16 w-16 text-gray-400 mx-auto" />
          
          <div>
            <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              {isDragActive ? '松开鼠标上传文件' : '拖拽文件到此处或点击上传'}
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              支持 Excel (.xlsx, .xls)、CSV (.csv)、TSV (.tsv)、ODS (.ods) 格式
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
              最大文件大小：20MB
            </p>
          </div>

          <div className="flex justify-center space-x-8 text-sm text-gray-500 dark:text-gray-400">
            <div className="flex items-center space-x-2">
              <FileText className="h-4 w-4" />
              <span>智能表头识别</span>
            </div>
            <div className="flex items-center space-x-2">
              <FileText className="h-4 w-4" />
              <span>自动数据清洗</span>
            </div>
            <div className="flex items-center space-x-2">
              <FileText className="h-4 w-4" />
              <span>AI图表推荐</span>
            </div>
          </div>
        </div>
      </div>

      {fileRejections.length > 0 && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div className="flex items-center space-x-2">
            <AlertCircle className="h-5 w-5 text-red-500" />
            <h4 className="font-medium text-red-800 dark:text-red-200">文件上传失败</h4>
          </div>
          <ul className="mt-2 text-sm text-red-700 dark:text-red-300">
            {fileRejections.map(({ file, errors }) => (
              <li key={file.name}>
                {file.name}: {errors.map(e => e.message).join(', ')}
              </li>
            ))}
          </ul>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div className="flex items-center space-x-2">
            <AlertCircle className="h-5 w-5 text-red-500" />
            <h4 className="font-medium text-red-800 dark:text-red-200">处理错误</h4>
          </div>
          <p className="mt-2 text-sm text-red-700 dark:text-red-300">{error}</p>
        </div>
      )}
    </div>
  )
}

export default FileUpload