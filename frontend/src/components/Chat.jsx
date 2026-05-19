import { useState } from 'react'
import axios from 'axios'

export default function Chat() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const ask = async () => {
    if (!question.trim() || loading) return
    setMessages(prev => [...prev, { role: 'user', text: question }])
    setQuestion('')
    setLoading(true)
    try {
      const res = await axios.post('https://rag-doc-qa-tzox.onrender.com/query', { question })
      setMessages(prev => [...prev, { role: 'bot', text: res.data.answer, sources: res.data.sources }])
    } catch {
      setMessages(prev => [...prev, { role: 'bot', text: 'Error contacting the API.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask() } }

  return (
    <div style={{display:'flex',flexDirection:'column',gap:'1rem'}}>
      <div className="messages">
        {messages.length === 0 && <p className="empty-msg">Upload a PDF above, then ask anything about it.</p>}
        {messages.map((msg, i) => (
          <div key={i} className={'bubble-wrap ' + msg.role}>
            <div className={'bubble ' + msg.role}>
              <p style={{margin:0,lineHeight:'1.6'}}>{msg.text}</p>
              {msg.sources?.length > 0 && (
                <div style={{marginTop:'8px',paddingTop:'8px',borderTop:'1px solid rgba(0,0,0,0.1)'}}>
                  <p style={{fontSize:'11px',color:'#94a3b8',margin:'0 0 4px'}}>Sources</p>
                  <div style={{display:'flex',flexWrap:'wrap',gap:'4px'}}>
                    {[...new Set(msg.sources.map(s => s.file))].map((file, j) => (
                      <span key={j} style={{
                        fontSize:'11px',background:'#f1f5f9',color:'#475569',
                        padding:'2px 8px',borderRadius:'20px',display:'inline-block'
                      }}>
                        📄 {file.replace(/^[a-f0-9]+_/, '')}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="bubble-wrap bot">
            <div className="typing">
              <div className="dot"/><div className="dot"/><div className="dot"/>
            </div>
          </div>
        )}
      </div>
      <div className="input-row">
        <textarea rows={2} placeholder="Ask a question about your document..." value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={handleKey}/>
        <button className="send-btn" onClick={ask} disabled={loading || !question.trim()}>Send</button>
      </div>
      <p className="hint">Enter to send · Shift+Enter for new line</p>
    </div>
  )
}