import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "gemma:7b")

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>INTEGRA V6</title>
  <script crossorigin src='https://unpkg.com/react@17/umd/react.development.js'></script>
  <script crossorigin src='https://unpkg.com/react-dom@17/umd/react-dom.development.js'></script>
  <script crossorigin src='https://unpkg.com/@babel/standalone/babel.min.js'></script>
  <style>body{margin:0;background:#000;color:#0f0;font-family:monospace}</style>
</head>
<body>
<div id='root'></div>
<script type='text/babel'>
{react_code}
ReactDOM.render(<IntegraDemo />, document.getElementById('root'));
</script>
</body>
</html>
"""

REACT_CODE = r"""
import React, { useState, useEffect, useRef } from 'react';

const IntegraDemo = () => {
  // État pour la date et l'heure
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isConnected, setIsConnected] = useState(true);
  
  // États pour les contrôles
  const [controls, setControls] = useState({
    microphone: false,
    streaming: false,
    internet: true,
    sudo: false,
    muteAgent: false
  });

  // États pour l'interface
  const [activeTab, setActiveTab] = useState('conversation');
  const [showTerminal, setShowTerminal] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showThinks, setShowThinks] = useState(false);
  const [stealthMode, setStealthMode] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showAgentSelect, setShowAgentSelect] = useState(false);
  const [showLLMSelect, setShowLLMSelect] = useState(false);

  // État pour la conversation
  const [messages, setMessages] = useState([
    { type: 'system', text: 'INTEGRA SYSTEM V6 INITIALIZED...', timestamp: new Date() },
    { type: 'system', text: 'Connexion à Ollama avec Gemma:7b...', timestamp: new Date() },
    { type: 'system', text: '✅ Système prêt - Mode démo actif', timestamp: new Date() }
  ]);
  const [inputText, setInputText] = useState('');
  const [currentMood, setCurrentMood] = useState('neutral');
  const [terminalInput, setTerminalInput] = useState('');
  const [terminalHistory, setTerminalHistory] = useState(['$ System ready...']);
  const [isTyping, setIsTyping] = useState(false);

  // Références
  const messagesEndRef = useRef(null);

  // Agents et LLMs
  const agents = [
    { id: 'integra', name: 'INTEGRA', personality: 'Déterminée, cynique, loyale' },
    { id: 'shadow', name: 'SHADOW', personality: 'Mystérieuse, calculatrice' },
    { id: 'nova', name: 'NOVA', personality: 'Énergique, optimiste' }
  ];

  const llms = [
    { id: 'gemma:7b', name: 'Gemma', size: '7B', status: 'active' },
    { id: 'llama3:8b', name: 'Llama 3', size: '8B', status: 'available' },
    { id: 'mistral:7b', name: 'Mistral', size: '7B', status: 'available' }
  ];

  const [selectedAgent, setSelectedAgent] = useState(agents[0]);
  const [selectedLLM, setSelectedLLM] = useState(llms[0]);

  // Réponses pré-définies pour la démo
  const demoResponses = {
    'integra': [
      "Hmm... intéressant. Tu veux vraiment que je fasse ça, Anansi?",
      "Tch, c'est tout ce que tu as à me donner? Allez, fais mieux que ça.",
      "Heh, pas mal. Mais je sais que tu peux faire beaucoup mieux.",
      "Tu me poses cette question maintenant? J'espère que tu es prêt pour la réponse...",
      "Vraiment? C'est ça ton grand défi du jour? Heh, très bien, jouons."
    ],
    'shadow': [
      "Les ombres révèlent toujours plus que la lumière... Que cherches-tu vraiment?",
      "Dans le silence entre tes mots, je perçois une vérité cachée.",
      "Chaque question contient sa propre réponse. Il suffit de savoir écouter.",
      "L'obscurité n'est pas l'absence de lumière, mais la présence du mystère.",
      "Tu navigues entre les mondes visibles et invisibles... intéressant."
    ],
    'nova': [
      "Oh wow! C'est une super question! ✨ Je suis tellement excitée de t'aider!",
      "YES! On va faire des trucs incroyables ensemble! 🚀",
      "Tu sais quoi? Tu es génial! Cette idée va être fantastique! 💫",
      "J'ADORE ton énergie! Allez, on fonce et on fait de la magie! ⭐",
      "C'est parti pour l'aventure! Je sens qu'on va créer quelque chose d'exceptionnel! 🌟"
    ]
  };

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const addSystemMessage = (text) => {
    setMessages(prev => [...prev, { type: 'system', text, timestamp: new Date() }]);
  };

  const toggleControl = (control) => {
    const newState = !controls[control];
    setControls(prev => ({ ...prev, [control]: newState }));
    switch(control) {
      case 'microphone':
        addSystemMessage(newState ? '🎤 Microphone activé - Mode démo' : '🎤 Microphone désactivé');
        break;
      case 'streaming':
        addSystemMessage(newState ? '📹 Capture d\'écran activée' : '📹 Capture d\'écran désactivée');
        break;
      case 'internet':
        addSystemMessage(newState ? '🌐 Accès Internet activé' : '🌐 Mode hors ligne');
        break;
      case 'sudo':
        addSystemMessage(newState ? '⚡ SUDO MODE ACTIVÉ - Contrôle système complet' : '⚡ Sudo mode désactivé');
        break;
      case 'muteAgent':
        addSystemMessage(newState ? '🔇 Agent muté' : '🔊 Agent peut parler');
        break;
    }
  };

  const generateDemoResponse = (message) => {
    const agentResponses = demoResponses[selectedAgent.id];
    const randomResponse = agentResponses[Math.floor(Math.random() * agentResponses.length)];
    let mood = 'neutral';
    if (message.includes('?')) mood = 'thinking';
    if (message.includes('!')) mood = 'excited';
    if (message.toLowerCase().includes('analyse')) mood = 'analyzing';
    if (message.toLowerCase().includes('défi')) mood = 'challenging';
    return { response: randomResponse, mood };
  };

  const sendMessage = async (text = inputText) => {
    if (!text.trim()) return;
    setMessages(prev => [...prev, { type: 'user', text, timestamp: new Date() }]);
    setInputText('');
    setIsTyping(true);
    setTimeout(() => {
      const { response, mood } = generateDemoResponse(text);
      setCurrentMood(mood);
      setMessages(prev => [...prev, { type: 'ai', text: response, mood, timestamp: new Date() }]);
      setIsTyping(false);
    }, 1000 + Math.random() * 2000);
  };

  const executeTerminalCommand = async () => {
    if (!terminalInput.trim()) return;
    const command = terminalInput.trim();
    setTerminalHistory(prev => [...prev, `$ ${command}`]);
    setTerminalInput('');
    if (!controls.sudo) {
      setTerminalHistory(prev => [...prev, '❌ Erreur: Sudo mode requis']);
      return;
    }
    if (command === 'help') {
      setTerminalHistory(prev => [...prev, 'Commandes disponibles:', '  status    - Afficher le statut système', '  clear     - Nettoyer le terminal', '  demo      - Mode démonstration']);
    } else if (command === 'clear') {
      setTerminalHistory(['$ System ready...']);
    } else if (command === 'status') {
      setTerminalHistory(prev => [...prev, `Agent: ${selectedAgent.name}`, `Modèle: ${selectedLLM.id}`, `Mood: ${currentMood}`, 'Mode: Démonstration']);
    } else if (command === 'demo') {
      setTerminalHistory(prev => [...prev, 'MODE DÉMO - Toutes les fonctions sont simulées']);
    } else {
      setTerminalHistory(prev => [...prev, `Commande simulée: ${command} [Mode démo]`]);
    }
  };

  const ControlButton = ({ icon, name, controlKey, title }) => (
    <div className={`control-item ${controls[controlKey] ? 'active' : ''}`} onClick={() => toggleControl(controlKey)} title={title}>
      <span className="control-icon">{icon}</span>
      <span className="control-name">{name}</span>
      <div className="control-status"></div>
    </div>
  );

  const InterfaceButton = ({ icon, name, active, onClick, title }) => (
    <div className={`interface-item ${active ? 'active' : ''}`} onClick={onClick} title={title}>
      <span className="interface-icon">{icon}</span>
      <span className="interface-name">{name}</span>
      <div className="interface-status"></div>
    </div>
  );

  return (
    <div className="integra-app">
      <div className="header">
        <div className="header-left">
          <div className="logo-container">
            <div className="logo-circle">
              <div className="logo-inner"></div>
            </div>
            <div className="logo-text">INTEGRA</div>
          </div>
        </div>
        <div className="header-center">
          <div className="header-title">
            <span className="header-icon">🎯</span>
            INTEGRA SYSTEM V6.0 - DEMO MODE
          </div>
        </div>
        <div className="header-right">
          <div className="status-indicators">
            <span className={`status-dot ${isConnected ? 'online' : 'offline'}`}></span>
            <span className="status-text">DEMO</span>
            <span className="status-memory">Memory: 2.4GB</span>
            <span className="status-cpu">CPU: 45%</span>
            <span className="datetime">
              {currentTime.toLocaleDateString('fr-FR')} | {currentTime.toLocaleTimeString('fr-FR')}
            </span>
          </div>
        </div>
      </div>

      <div className="main-content">
        <div className="sidebar-left">
          <div className="section-title">MAIN CONTROLS</div>
          <div className="controls-section">
            <ControlButton icon="🎤" name="Microphone" controlKey="microphone" title="Activer/Désactiver l'écoute vocale" />
            <ControlButton icon="📹" name="Streaming" controlKey="streaming" title="Capture d'écran pour analyse" />
            <ControlButton icon="🌐" name="Internet" controlKey="internet" title="Accès Internet" />
            <ControlButton icon="⚡" name="Sudo Mode" controlKey="sudo" title="Contrôle système complet" />
            <ControlButton icon="🔇" name="Mute Agent" controlKey="muteAgent" title="Couper la voix de l'IA" />
          </div>

          <div className="section-title">INTERFACE</div>
          <div className="interface-section">
            <InterfaceButton icon="💬" name="Conversation" active={activeTab === 'conversation'} onClick={() => setActiveTab('conversation')} />
            <InterfaceButton icon="📁" name="History" active={showHistory} onClick={() => setShowHistory(!showHistory)} />
            <InterfaceButton icon="💻" name="Terminal" active={showTerminal} onClick={() => setShowTerminal(!showTerminal)} />
            <InterfaceButton icon="🤖" name="Show Thinks" active={showThinks} onClick={() => setShowThinks(!showThinks)} />
            <InterfaceButton icon="🥷" name="Stealth Mode" active={stealthMode} onClick={() => setStealthMode(!stealthMode)} />
          </div>
        </div>

        <div className="content-center">
          <div className="motto">FIGHT OR BE NOTHING</div>
          <div className="chat-container">
            <div className="chat-messages">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.type}`}>
                  <div className="message-header">
                    <span className="message-author">
                      {msg.type === 'user' ? 'USER' : msg.type === 'system' ? 'SYSTEM' : selectedAgent.name}
                    </span>
                    <span className="message-time">
                      {msg.timestamp.toLocaleTimeString('fr-FR')}
                    </span>
                  </div>
                  <div className="message-content">{msg.text}</div>
                  {msg.mood && showThinks && <div className="message-mood">[Mood: {msg.mood}]</div>}
                </div>
              ))}
              {isTyping && (
                <div className="message ai typing">
                  <div className="typing-indicator"><span></span><span></span><span></span></div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            <div className="chat-input-container">
              <input type="text" className="chat-input" placeholder="Qu'est-ce que tu veux, Anansi..." value={inputText} onChange={(e) => setInputText(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendMessage()} />
              <button className="send-button" onClick={() => sendMessage()} disabled={!inputText.trim()}>SEND</button>
            </div>
          </div>

          {showTerminal && (
            <div className="terminal-container">
              <div className="terminal-header"><span>TERMINAL - DEMO MODE</span><button onClick={() => setShowTerminal(false)}>✕</button></div>
              <div className="terminal-content">
                {terminalHistory.map((line, index) => (<div key={index} className="terminal-line">{line}</div>))}
              </div>
              <div className="terminal-input-container">
                <span className="terminal-prompt">$</span>
                <input type="text" className="terminal-input" value={terminalInput} onChange={(e) => setTerminalInput(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && executeTerminalCommand()} placeholder="Tapez 'help' pour les commandes..." />
              </div>
            </div>
          )}
        </div>

        <div className="sidebar-right">
          <div className="hologram-container">
            <div className={`hologram-display mood-${currentMood}`}>
              <div className="hologram-figure">
                <div className="hologram-avatar">
                  <div className="avatar-core"></div>
                  <div className="avatar-ring"></div>
                  <div className="avatar-particles"></div>
                </div>
                <div className="hologram-effects">
                  <div className="hologram-scanlines"></div>
                  <div className="hologram-glitch"></div>
                  <div className="hologram-pulse"></div>
                </div>
              </div>
              <div className="hologram-info">
                <h3>{selectedAgent.name}</h3>
                <p className="hologram-status"><span className="status-dot online"></span>{isTyping ? 'Processing...' : 'Listening...'}</p>
                <p className="hologram-mood">Mood: {currentMood}</p>
              </div>
            </div>

            <div className="media-controls">
              <button className="media-button" onClick={() => setShowAgentSelect(!showAgentSelect)}><span>🎭</span> SELECT AGENT</button>
              <button className="media-button" onClick={() => setShowLLMSelect(!showLLMSelect)}><span>🧠</span> SELECT LLM</button>
              <button className="media-button" onClick={() => setShowSettings(!showSettings)}><span>⚙️</span> SETTINGS</button>
            </div>
            <div className="media-button-container"><button className="customize-button">CUSTOMIZE MOOD MEDIA</button></div>
          </div>
        </div>
      </div>

      {showAgentSelect && (
        <div className="modal-overlay" onClick={() => setShowAgentSelect(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header"><h2>SELECT AGENT</h2><button onClick={() => setShowAgentSelect(false)}>✕</button></div>
            <div className="modal-content">
              {agents.map(agent => (
                <div key={agent.id} className={`agent-option ${selectedAgent.id === agent.id ? 'selected' : ''}`} onClick={() => { setSelectedAgent(agent); setShowAgentSelect(false); addSystemMessage(`Agent changé: ${agent.name}`); }}>
                  <div className="agent-name">{agent.name}</div>
                  <div className="agent-personality">{agent.personality}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {showLLMSelect && (
        <div className="modal-overlay" onClick={() => setShowLLMSelect(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header"><h2>SELECT LLM</h2><button onClick={() => setShowLLMSelect(false)}>✕</button></div>
            <div className="modal-content">
              {llms.map(llm => (
                <div key={llm.id} className={`llm-option ${selectedLLM.id === llm.id ? 'selected' : ''}`} onClick={() => { setSelectedLLM(llm); setShowLLMSelect(false); addSystemMessage(`Modèle changé: ${llm.name} (${llm.size})`); }}>
                  <div className="llm-name">{llm.name}</div>
                  <div className="llm-size">{llm.size}</div>
                  <div className={`llm-status ${llm.status}`}>{llm.status}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .integra-app { width: 100%; height: 100vh; background: #000; color: #00ff00; font-family: 'Courier New', monospace; display: flex; flex-direction: column; overflow: hidden; }
        .header { height: 60px; border-bottom: 2px solid #00ff00; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; background: rgba(0, 255, 0, 0.05); }
        .header-left { display: flex; align-items: center; }
        .logo-container { display: flex; align-items: center; gap: 15px; }
        .logo-circle { width: 40px; height: 40px; border: 2px solid #00ff00; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; animation: pulse 2s infinite; }
        .logo-inner { width: 20px; height: 20px; background: #00ff00; border-radius: 50%; animation: glow 2s infinite; }
        .logo-text { font-size: 24px; font-weight: bold; letter-spacing: 2px; }
        .header-center { flex: 1; display: flex; justify-content: center; }
        .header-title { font-size: 18px; display: flex; align-items: center; gap: 10px; }
        .header-icon { font-size: 24px; }
        .header-right { display: flex; align-items: center; }
        .status-indicators { display: flex; align-items: center; gap: 20px; font-size: 12px; }
        .status-dot { width: 8px; height: 8px; border-radius: 50%; animation: blink 2s infinite; }
        .status-dot.online { background: #00ff00; }
        .status-dot.offline { background: #ff0000; }
        .datetime { color: #00ffff; font-weight: bold; margin-left: 20px; }
        .main-content { flex: 1; display: flex; overflow: hidden; }
        .sidebar-left { width: 300px; background: rgba(0, 255, 0, 0.02); border-right: 1px solid #00ff00; padding: 20px; overflow-y: auto; }
        .section-title { font-size: 12px; color: #666; margin-bottom: 15px; letter-spacing: 1px; }
        .control-item, .interface-item { display: flex; align-items: center; padding: 12px; margin-bottom: 8px; border: 1px solid #333; border-radius: 4px; cursor: pointer; transition: all 0.3s; position: relative; }
        .control-item:hover, .interface-item:hover { border-color: #00ff00; background: rgba(0, 255, 0, 0.05); }
        .control-item.active, .interface-item.active { border-color: #ffd700; background: rgba(255, 215, 0, 0.1); }
        .control-icon, .interface-icon { font-size: 20px; margin-right: 12px; }
        .control-name, .interface-name { flex: 1; font-size: 14px; }
        .control-status, .interface-status { width: 8px; height: 8px; border-radius: 50%; background: #333; }
        .control-item.active .control-status, .interface-item.active .interface-status { background: #ffd700; box-shadow: 0 0 10px #ffd700; }
        .content-center { flex: 1; display: flex; flex-direction: column; padding: 20px; overflow: hidden; }
        .motto { text-align: center; font-size: 36px; font-weight: bold; color: #00ff00; text-shadow: 0 0 20px #00ff00; margin-bottom: 20px; letter-spacing: 4px; }
        .chat-container { flex: 1; display: flex; flex-direction: column; border: 1px solid #00ff00; border-radius: 8px; overflow: hidden; background: rgba(0, 255, 0, 0.02); }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; }
        .message { margin-bottom: 15px; padding: 12px; border-radius: 4px; border: 1px solid #333; }
        .message.user { background: rgba(0, 255, 0, 0.05); border-color: #00ff00; }
        .message.ai { background: rgba(255, 215, 0, 0.05); border-color: #ffd700; }
        .message.system { background: rgba(255, 255, 255, 0.05); border-color: #666; text-align: center; font-style: italic; }
        .message-header { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 12px; opacity: 0.7; }
        .message-content { font-size: 14px; line-height: 1.5; }
        .message-mood { margin-top: 8px; font-size: 11px; color: #666; font-style: italic; }
        .typing { display: flex; align-items: center; }
        .typing-indicator { display: flex; gap: 5px; }
        .typing-indicator span { width: 8px; height: 8px; background: #ffd700; border-radius: 50%; animation: typingDot 1.4s infinite; }
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        .chat-input-container { display: flex; padding: 15px; border-top: 1px solid #00ff00; background: rgba(0, 255, 0, 0.02); }
        .chat-input { flex: 1; padding: 12px; background: #000; border: 1px solid #00ff00; color: #00ff00; font-family: 'Courier New', monospace; font-size: 14px; outline: none; }
        .send-button { margin-left: 10px; padding: 12px 30px; background: #00ff00; color: #000; border: none; font-weight: bold; cursor: pointer; font-family: 'Courier New', monospace; transition: all 0.3s; }
        .send-button:hover:not(:disabled) { background: #ffd700; box-shadow: 0 0 20px #ffd700; }
        .send-button:disabled { opacity: 0.5; cursor: not-allowed; }
        .terminal-container { margin-top: 20px; height: 200px; border: 1px solid #00ff00; border-radius: 4px; overflow: hidden; background: #000; }
        .terminal-header { display: flex; justify-content: space-between; padding: 10px; background: #00ff00; color: #000; font-weight: bold; }
        .terminal-content { height: 120px; padding: 10px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 12px; }
        .terminal-line { margin-bottom: 5px; color: #00ff00; }
        .terminal-input-container { display: flex; padding: 10px; border-top: 1px solid #00ff00; }
        .terminal-prompt { margin-right: 10px; color: #00ff00; }
        .terminal-input { flex: 1; background: transparent; border: none; color: #00ff00; font-family: 'Courier New', monospace; outline: none; }
        .sidebar-right { width: 400px; background: rgba(0, 255, 0, 0.02); border-left: 1px solid #00ff00; padding: 20px; display: flex; flex-direction: column; }
        .hologram-container { flex: 1; display: flex; flex-direction: column; }
        .hologram-display { flex: 1; border: 2px solid #00ff00; border-radius: 8px; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(0, 255, 0, 0.02); position: relative; overflow: hidden; }
        .hologram-figure { position: relative; width: 250px; height: 300px; display: flex; align-items: center; justify-content: center; }
        .hologram-avatar { position: relative; width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; }
        .avatar-core { width: 80px; height: 80px; background: linear-gradient(45deg, #00ff00, #00ffff); border-radius: 50%; animation: coreRotate 4s linear infinite; }
        .avatar-ring { position: absolute; width: 120px; height: 120px; border: 2px solid #00ff00; border-radius: 50%; border-top-color: transparent; animation: ringSpin 3s linear infinite; }
        .avatar-particles { position: absolute; width: 100%; height: 100%; background: radial-gradient(circle, rgba(0,255,0,0.1) 0%, transparent 70%); animation: particles 2s ease-in-out infinite alternate; }
        .hologram-effects { position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; }
        .hologram-scanlines { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 255, 255, 0.03) 2px, rgba(0, 255, 255, 0.03) 4px); animation: scanlines 8s linear infinite; }
        .hologram-glitch { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(45deg, transparent 30%, rgba(0, 255, 255, 0.1) 50%, transparent 70%); animation: glitch 5s linear infinite; }
        .hologram-pulse { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 300px; height: 300px; border: 2px solid rgba(0, 255, 255, 0.3); border-radius: 50%; animation: pulse 2s ease-in-out infinite; }
        .hologram-info { margin-top: 20px; text-align: center; }
        .hologram-info h3 { font-size: 24px; color: #00ffff; text-shadow: 0 0 10px #00ffff; margin: 0; }
        .hologram-status { display: flex; align-items: center; justify-content: center; gap: 10px; margin: 10px 0; font-size: 14px; color: #00ff00; }
        .hologram-mood { font-size: 12px; color: #ffd700; }
        .mood-thinking .hologram-display { border-color: #ffd700; }
        .mood-thinking .avatar-core { background: linear-gradient(45deg, #ffd700, #ffff00); }
        .mood-challenging .hologram-display { border-color: #ff6600; }
        .mood-challenging .avatar-core { background: linear-gradient(45deg, #ff6600, #ff0000); }
        .mood-excited .hologram-display { border-color: #00ffff; }
        .mood-excited .avatar-core { background: linear-gradient(45deg, #00ffff, #0080ff); }
        .mood-analyzing .hologram-display { border-color: #ff00ff; }
        .mood-analyzing .avatar-core { background: linear-gradient(45deg, #ff00ff, #8000ff); }
        .media-controls { margin-top: 20px; display: flex; flex-direction: column; gap: 10px; }
        .media-button { padding: 12px; background: rgba(0, 255, 0, 0.1); border: 1px solid #00ff00; color: #00ff00; cursor: pointer; font-family: 'Courier New', monospace; font-size: 14px; transition: all 0.3s; display: flex; align-items: center; gap: 10px; }
        .media-button:hover { background: rgba(0, 255, 0, 0.2); box-shadow: 0 0 10px #00ff00; }
        .media-button-container { margin-top: 20px; }
        .customize-button { width: 100%; padding: 15px; background: #00ff00; color: #000; border: none; font-weight: bold; cursor: pointer; font-family: 'Courier New', monospace; transition: all 0.3s; }
        .customize-button:hover { background: #ffd700; box-shadow: 0 0 20px #ffd700; }
        .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.8); display: flex; align-items: center; justify-content: center; z-index: 1000; }
        .modal { background: #000; border: 2px solid #00ff00; border-radius: 8px; padding: 20px; width: 500px; max-width: 90%; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .modal-header h2 { color: #00ff00; font-size: 20px; }
        .modal-header button { background: transparent; border: none; color: #00ff00; font-size: 24px; cursor: pointer; }
        .agent-option, .llm-option { padding: 15px; border: 1px solid #333; margin-bottom: 10px; cursor: pointer; transition: all 0.3s; }
        .agent-option:hover, .llm-option:hover { border-color: #00ff00; background: rgba(0, 255, 0, 0.05); }
        .agent-option.selected, .llm-option.selected { border-color: #ffd700; background: rgba(255, 215, 0, 0.1); }
        .agent-personality, .llm-size { font-size: 12px; color: #666; margin-top: 5px; }
        .llm-status { font-size: 11px; margin-top: 5px; }
        .llm-status.active { color: #00ff00; }
        .llm-status.available { color: #ffd700; }
        @keyframes pulse { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.1); opacity: 0.7; } 100% { transform: scale(1); opacity: 1; } }
        @keyframes glow { 0% { box-shadow: 0 0 5px #00ff00; } 50% { box-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00; } 100% { box-shadow: 0 0 5px #00ff00; } }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        @keyframes typingDot { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-10px); } }
        @keyframes coreRotate { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes ringSpin { 0% { transform: rotate(0deg); } 100% { transform: rotate(-360deg); } }
        @keyframes particles { 0% { opacity: 0.3; } 100% { opacity: 0.8; } }
        @keyframes scanlines { 0% { transform: translateY(0); } 100% { transform: translateY(10px); } }
        @keyframes glitch { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #000; }
        ::-webkit-scrollbar-thumb { background: #00ff00; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #ffd700; }
      `}</style>
    </div>
  );
};

export default IntegraDemo;
"""

@app.route('/')
def index():
    return HTML_TEMPLATE.format(react_code=REACT_CODE)

@app.route('/api/status')
def status():
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags")
        r.raise_for_status()
        models = [m.get('name') for m in r.json().get('models', [])]
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500
    return jsonify({'status': 'ok', 'models': models})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    prompt = data.get('prompt', '')
    model = data.get('model', DEFAULT_MODEL)
    payload = {'model': model, 'prompt': prompt, 'stream': False}
    try:
        r = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=60)
        r.raise_for_status()
        response = r.json().get('response', '')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
