import { useState } from 'react'
import Upload from './components/Upload'
import Chat from './components/Chat'
import './index.css'

export default function App() {
  const [docInfo, setDocInfo] = useState(null)
  return (
    <div>
      <div className="card">
        <div className="app-title">
          <h1>RAG Document Q&A</h1>
          <p>Upload a PDF · Ask questions · Get cited answers</p>
        </div>
        <Upload onUploadSuccess={setDocInfo} />
        {docInfo && (
          <div className="doc-info">
            📂 <strong>{docInfo.filename}</strong> · {docInfo.chunks_indexed} chunks indexed
          </div>
        )}
        <hr className="divider" />
        <Chat />
      </div>
    </div>
  )
}
