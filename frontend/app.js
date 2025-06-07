async function sendPrompt(prompt) {
  const res = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt })
  });
  const data = await res.json();
  const div = document.createElement('div');
  div.textContent = 'AI: ' + data.response;
  document.body.appendChild(div);
}

sendPrompt('Hello from frontend');
