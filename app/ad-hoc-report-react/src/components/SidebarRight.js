import React from 'react';

export default function SidebarRight() {
  return (
    <div className="right-panel">
      {/* Species */}
      <div className="section-header">
        <span>Species</span><span>≡</span>
      </div>
      <div className="filter-section">
        {['Cachorro', 'Gato', 'Coelho', 'Outros'].map((spec, i) => (
          <label key={i} className="filter-item">
            <input type="checkbox" defaultChecked={i < 2} />
            {spec}
          </label>
        ))}
      </div>

      {/* Status */}
      <div className="section-header">
        <span>Status</span><span>≡</span>
      </div>
      <div className="filter-section">
        {['Disponível', 'Adotado', 'Pendente'].map((st, i) => (
          <label key={i} className="filter-item">
            <input type="checkbox" defaultChecked={i === 0} />
            {st}
          </label>
        ))}
      </div>

      {/* Faixa Etária */}
      <div className="section-header">
        <span>Faixa Etária</span><span>≡</span>
      </div>
      <div className="filter-section">
        {['Filhote', 'Jovem', 'Adulto', 'Idoso'].map((age, i) => (
          <label key={i} className="filter-item">
            <input type="checkbox" defaultChecked />
            {age}
          </label>
        ))}
      </div>
    </div>
  );
}
