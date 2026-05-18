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
      const res = await axios.post('http://localhost:8000/query', { question })
      setMessages(prev => [...prev, { role: 'bot', text: res.data.answer, sources: res.data.sources }])
    } catch {
      setMessages(prev => [...prev, { role: 'bot', text: 'Error contacting the API.' }])
    } finally { setLoading(false) }
  }

  const handleKey = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask() } }

  return (
    <div style={{display:'flex',flexDirection:'column',gap:'1rem'}}>
      <div className="messages">
        {messages.length === 0 && <p className="empty-msg">Upload a PDF above, then ask anything about it.</p>}
        {messages.map((msg, i) => (
          <div key={i} className={'bubble-wrap ' + msg.role}>
            <div className={'bubble ' + msg.role}>
              {msg.text}
              {msg.sources?.length > 0 && (
                <div className="sources">
                  {msg.sources.map((s, j) => <span key={j} style={{marginRight:'0.5rem'}}>📎 {s.file} p.{s.page}</span>)}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && <div className="bubble-wrap bot"><div className="typing"><div className="dot"/><div className="dot"/><div className="dot"/></div></div>}
      </div>
      <div className="input-row">
        <textarea rows={2} placeholder="Ask a question about your document..." value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={handleKey}/>
        <button className="send-btn" onClick={ask} disabled={loading || !question.trim()}>Send</button>
      </div>
      <p className="hint">Enter to send · Shift+Enter for new line</p>
    </div>
  )
}
