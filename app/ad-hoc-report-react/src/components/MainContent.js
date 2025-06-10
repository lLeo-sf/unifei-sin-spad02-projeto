import React, { useState } from 'react';

export default function MainContent() {
  const [columns, setColumns] = useState([]);
  const [groups, setGroups] = useState([]);

  const onDragOver = e => e.preventDefault();

  const onDrop = (target) => (e) => {
    e.preventDefault();
    const field = e.dataTransfer.getData('text/plain');
    if (!field) return;
    const setter = target === 'columns' ? setColumns : setGroups;
    const list = target === 'columns' ? columns : groups;
    if (!list.includes(field)) setter(prev => [...prev, field]);
  };

  const remove = (target, item) => {
    const setter = target === 'columns' ? setColumns : setGroups;
    setter(prev => prev.filter(f => f !== item));
  };

  return (
    <div className="center-panel">
      <div className="toolbar">
        <button title="Run Report">▶️</button>
        <button title="Export to Excel">📊</button>
        <button title="Export to PDF">📄</button>
        <button title="Export to CSV">📁</button>
        <button title="Print">🖨️</button>
        <select>
          <option>Table</option>
          <option>Pivot</option>
        </select>
        <select>
          <option>Full Data</option>
          <option>Summary</option>
        </select>
      </div>

      <div
        className="report-section"
        onDragOver={onDragOver}
        onDrop={onDrop('columns')}
      >
        <div className="section-title">Colunas</div>
        <div className="drop-zone">
          {columns.map(f => (
            <div key={f} className="dropped-item">
              {f}
              <button
                className="remove-btn"
                onClick={() => remove('columns', f)}
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      </div>

      <div
        className="report-section"
        onDragOver={onDragOver}
        onDrop={onDrop('groups')}
      >
        <div className="section-title">Agrupamentos</div>
        <div className="drop-zone">
          {groups.map(f => (
            <div key={f} className="dropped-item">
              {f}
              <button
                className="remove-btn"
                onClick={() => remove('groups', f)}
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="report-title">Relatório de Animais para Adoção</div>
      {/* Aqui você pode renderizar sua tabela dinamicamente com `columns` e `groups` */}
      <table className="result-table">
        <thead>
          <tr>
            {columns.map(c => (
              <th key={c} className="column-header">{c}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {/* rows... */}
        </tbody>
      </table>

      <div className="status-bar">
        {columns.length} colunas selecionadas | Última atualização: 06/05/2025 14:30
      </div>
    </div>
  );
}
