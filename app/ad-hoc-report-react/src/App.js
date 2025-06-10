import React from 'react';
import Header from './components/Header';
import SidebarLeft from './components/SidebarLeft';
import MainContent from './components/MainContent';
import SidebarRight from './components/SidebarRight';
import './index.css';

function App() {
  return (
    <div>
      <Header />
      <div className="topic-header">
        <span className="topic-title">Tópico: Adoção de Animais</span>
        <button onClick={() => alert('Criar novo relatório ad hoc')}>Nova View</button>
      </div>
      <div className="main-container">
        <SidebarLeft />
        <MainContent />
        <SidebarRight />
      </div>
    </div>
  );
}

export default App;
