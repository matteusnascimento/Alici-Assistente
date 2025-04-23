import React, { useState } from 'react';

function App() {
  const [message,  setMessage]  = useState('');
  const [response, setResponse] = useState('');

  const sendMessage = async () => {
    const res = await fetch('/api/message', {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({ sender:'Usuário', message })
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-4">Alici Empreendedora</h1>
      <textarea
        value={message}
        onChange={e => setMessage(e.target.value)}
        placeholder="Digite sua mensagem..."
        className="w-full max-w-md p-2 border rounded mb-4"
      />
      <button
        onClick={sendMessage}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Enviar
      </button>
      {response && <div className="mt-4 text-lg">{response}</div>}
    </div>
  );
}

export default App;
