import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

export default function Upload({ onUploadSuccess }) {
  const [status, setStatus] = useState('idle')
  const [filename, setFilename] = useState('')

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return
    setStatus('uploading')
    setFilename(file.name)
    const formData = new FormData()
    formData.append('file', file)
    try {
      const res = await axios.post('http://localhost:8000/upload', formData)
      setStatus('done')
      onUploadSuccess(res.data)
    } catch { setStatus('error') }
  }, [onUploadSuccess])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { 'application/pdf': ['.pdf'] }, multiple: false,
  })

  return (
    <div>
      <div {...getRootProps()} className={'dropzone' + (isDragActive ? ' active' : '')}>
        <input {...getInputProps()} />
        <div className="icon">📄</div>
        {isDragActive
          ? <p>Drop the PDF here...</p>
          : <p>Drag & drop a PDF, or <span>click to browse</span></p>}
        <small>Only PDF files supported</small>
      </div>
      {status === 'uploading' && <div className="status-msg uploading"><div className="spinner"/> Indexing <strong>{filename}</strong>...</div>}
      {status === 'done' && <div className="status-msg done">✅ <strong>{filename}</strong> indexed — ask a question below</div>}
      {status === 'error' && <div className="status-msg error">❌ Upload failed. Is the backend running?</div>}
    </div>
  )
}
