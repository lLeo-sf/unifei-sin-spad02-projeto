import React, { useState } from 'react';

const TABLES = {
  animais: [
    'animais.id',
    'animais.name',
    'animais.sex',
    'animais.ageGroup',
    'animais.breedString',
    'animais.statusId',
    'animais.adoptionFeeString',
  ],
  especies: [
    'especies.id',
    'especies.name',
    'especies.description',
  ],
  organizacoes: [
    'organizacoes.id',
    'organizacoes.name',
    'organizacoes.city',
    'organizacoes.state',
    'organizacoes.phone',
    'organizacoes.email',
  ],
  medidas: ['COUNT', 'SUM', 'AVG'],
};

export default function SidebarLeft() {
  const [open, setOpen] = useState({
    animais: true,
    especies: true,
    organizacoes: true,
    medidas: true,
  });

  const toggle = (sec) =>
    setOpen(o => ({ ...o, [sec]: !o[sec] }));

  const onDragStart = (e, field) => {
    e.dataTransfer.setData('text/plain', field);
  };

  return (
    <div className="left-panel">
      {Object.entries(TABLES).map(([section, fields]) => (
        <React.Fragment key={section}>
          <div
            className="section-header"
            onClick={() => toggle(section)}
          >
            <span>
              {section === 'animais' && 'Animais'}
              {section === 'especies' && 'Especies'}
              {section === 'organizacoes' && 'Organizações'}
              {section === 'medidas' && 'Medidas'}
            </span>
            <span>≡</span>
          </div>
          {open[section] && (
            <ul className="field-list" id={`${section}-section`}>
              {fields.map(f => (
                <li
                  key={f}
                  className="field-item"
                  draggable
                  onDragStart={e => onDragStart(e, f)}
                >
                  <span className="field-icon">
                    {section === 'medidas' ? '📈' : '📊'}
                  </span>
                  {f}
                </li>
              ))}
            </ul>
          )}
        </React.Fragment>
      ))}
    </div>
  );
}
