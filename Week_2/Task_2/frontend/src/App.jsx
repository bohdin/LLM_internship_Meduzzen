import { useEffect, useRef, useState } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const socketRef = useRef(null);

  const connectSocket = () => {
    socketRef.current = new WebSocket('ws://localhost:8000/stream');

    socketRef.current.onopen = () => {
      console.log('✅ WebSocket connected');
    };

    socketRef.current.onmessage = (event) => {
      const chunk = event.data;

      if (chunk.includes("[response interrupted]") || chunk.includes("[previous response cancelled]")) {
        setIsStreaming(false);
        return; // не додаємо це у повідомлення
      }

      setMessages((prev) => {
        if (prev.length === 0 || prev[prev.length - 1].sender !== 'ai') {
          return [...prev, { sender: 'ai', text: chunk }];
        } else {
          const lastMessage = prev[prev.length - 1];
          const newText = lastMessage.text + chunk;

          // запобігаємо дублюванню chunk
          if (newText.endsWith(chunk + chunk)) {
            return prev;
          }

          const newMessages = [...prev];
          newMessages[newMessages.length - 1] = {
            sender: 'ai',
            text: newText,
          };
          return newMessages;
        }
      });
    };

    socketRef.current.onclose = () => {
      console.log('❌ WebSocket disconnected');
      setIsStreaming(false);
    };
  };

  useEffect(() => {
    connectSocket();

    return () => {
      socketRef.current?.close();
    };
  }, []);

  const sendMessage = () => {
    if (!input.trim()) return;
    if (socketRef.current?.readyState !== WebSocket.OPEN) {
      console.warn('WebSocket is not open');
      return;
    }

    socketRef.current.send(input);
    setMessages((prev) => [...prev, { sender: 'user', text: input }]);
    setInput('');
    setIsStreaming(true);
  };

  const stopStreaming = () => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send("__STOP__");
      console.log("🛑 Stop signal sent");
      setIsStreaming(false);
    }
  };

  return (
    <div
      style={{
        height: '100vh',
        width: '100vw',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'Arial, sans-serif',
        backgroundColor: '#f5f5f5',
        padding: '1rem',
        boxSizing: 'border-box',
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '700px',
          backgroundColor: 'white',
          borderRadius: '10px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
          display: 'flex',
          flexDirection: 'column',
          height: '80vh',
          maxHeight: '800px',
          padding: '1rem',
          boxSizing: 'border-box',
        }}
      >
        <h2 style={{ margin: '0 0 1rem 0', textAlign: 'center' }}>LangChain Assistant</h2>
        <div
          style={{
            flexGrow: 1,
            overflowY: 'auto',
            padding: '1rem',
            border: '1px solid #ccc',
            borderRadius: '8px',
            whiteSpace: 'pre-wrap',
            marginBottom: '1rem',
            backgroundColor: '#fafafa',
          }}
        >
          {messages.map((msg, index) => (
            <div key={index} style={{ marginBottom: '1rem' }}>
              <strong>{msg.sender === 'user' ? 'You' : 'Assistant'}:</strong> {msg.text}
            </div>
          ))}
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
            style={{
              flex: 1,
              padding: '0.5rem 1rem',
              fontSize: '1rem',
              borderRadius: '6px',
              border: '1px solid #ccc',
              outline: 'none',
            }}
          />
          <button
            onClick={sendMessage}
            style={{
              padding: '0 1.5rem',
              fontSize: '1rem',
              borderRadius: '6px',
              border: 'none',
              backgroundColor: '#4f46e5',
              color: 'white',
              cursor: 'pointer',
              transition: 'background-color 0.3s',
            }}
            onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#4338ca')}
            onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#4f46e5')}
            disabled={isStreaming}
          >
            Send
          </button>
          <button
            onClick={stopStreaming}
            style={{
              padding: '0 1rem',
              fontSize: '1rem',
              borderRadius: '6px',
              border: '1px solid #e11d48',
              backgroundColor: '#fef2f2',
              color: '#b91c1c',
              cursor: 'pointer',
            }}
            disabled={!isStreaming}
          >
            ⏹ Stop
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
