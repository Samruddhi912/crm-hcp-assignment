import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addLog, addChatMessage } from './features/interactionSlice.js';

export default function App() {
  const dispatch = useDispatch();
  const chatHistory = useSelector((state) => state.interaction.chatHistory);
  
  const [formData, setFormData] = useState({ hcpName: '', type: 'Meeting', sentiment: 'Neutral', topics: '' });
  const [chatInput, setChatInput] = useState('');

  const handleFormSubmit = (e) => {
    e.preventDefault();
    dispatch(addLog(formData));
    alert("Form submitted manually!");
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    // Show user message immediately
    dispatch(addChatMessage({ sender: 'user', text: chatInput }));
    
    try {
      // Send message to FastAPI Backend
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: chatInput, thread_id: "user_123" })
      });
      const data = await response.json();
      
      // Show AI response
      dispatch(addChatMessage({ sender: 'ai', text: data.response }));
    } catch (error) {
      dispatch(addChatMessage({ sender: 'ai', text: 'Error connecting to backend.' }));
    }
    setChatInput('');
  };

  return (
    <div style={{ display: 'flex', fontFamily: 'Inter, sans-serif', height: '100vh', backgroundColor: '#f9f9f9', color: '#333' }}>
      
      {/* LEFT PANEL: Log Interaction Form */}
      <div style={{ flex: 2, padding: '30px', borderRight: '1px solid #ccc', backgroundColor: '#fff' }}>
        <h2 style={{ marginBottom: '20px' }}>Log HCP Interaction</h2>
        <form onSubmit={handleFormSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px', maxWidth: '500px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>HCP Name: </label>
            <input type="text" style={{ width: '100%', padding: '8px' }} value={formData.hcpName} onChange={e => setFormData({...formData, hcpName: e.target.value})} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Topics Discussed: </label>
            <textarea style={{ width: '100%', padding: '8px', minHeight: '100px' }} value={formData.topics} onChange={e => setFormData({...formData, topics: e.target.value})} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Sentiment: </label>
            <select style={{ width: '100%', padding: '8px' }} value={formData.sentiment} onChange={e => setFormData({...formData, sentiment: e.target.value})}>
              <option>Positive</option>
              <option>Neutral</option>
              <option>Negative</option>
            </select>
          </div>
          <button type="submit" style={{ padding: '10px', backgroundColor: '#0056b3', color: 'white', border: 'none', cursor: 'pointer', fontWeight: 'bold' }}>Log via Form</button>
        </form>
      </div>

      {/* RIGHT PANEL: AI Assistant Chat */}
      <div style={{ flex: 1, padding: '30px', display: 'flex', flexDirection: 'column', backgroundColor: '#fff' }}>
        <h2 style={{ marginBottom: '20px' }}>AI Assistant</h2>
        <div style={{ flex: 1, overflowY: 'auto', marginBottom: '15px', border: '1px solid #ddd', padding: '15px', borderRadius: '5px', backgroundColor: '#fafafa' }}>
          {chatHistory.length === 0 && <p style={{ color: '#888', textAlign: 'center' }}>Start typing to log an interaction...</p>}
          {chatHistory.map((msg, idx) => (
            <div key={idx} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left', margin: '10px 0' }}>
              <span style={{ display: 'inline-block', padding: '8px 12px', borderRadius: '15px', backgroundColor: msg.sender === 'user' ? '#0056b3' : '#e0e0e0', color: msg.sender === 'user' ? 'white' : 'black' }}>
                <strong>{msg.sender === 'user' ? 'You' : 'AI'}: </strong> {msg.text}
              </span>
            </div>
          ))}
        </div>
        <form onSubmit={handleChatSubmit} style={{ display: 'flex', gap: '10px' }}>
          <input 
            type="text" 
            value={chatInput} 
            onChange={e => setChatInput(e.target.value)} 
            placeholder="E.g. Met Dr. Smith, discussed Product X..." 
            style={{ flex: 1, padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
          />
          <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Send</button>
        </form>
      </div>
      
    </div>
  );
}